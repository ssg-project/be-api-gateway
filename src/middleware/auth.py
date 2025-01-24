from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
import os
import re
from typing import List
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

PUBLIC_PATHS = [
    "/health",
    "/user/api/v1/auth/login",
    "/user/api/v1/auth/join",
    "/event/api/v1/concert/list",
    r"/event/api/v1/concert/\d+"
]

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        try:
            self.redis_client = Redis(
                host=os.getenv('REDIS_HOST', '127.0.0.1'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=0,
                decode_responses=True
            )
        except Exception as e:
            raise

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        is_public = any(
            re.match(f"^{pattern}$", path)
            if pattern.startswith("/event/api/v1/concert/")
            else path == pattern
            for pattern in PUBLIC_PATHS
        )
        if is_public:
            return await call_next(request)
            
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="유효하지 않은 인증 헤더입니다.")
                
            token = auth_header.split(" ")[1]
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=[os.getenv("JWT_ALGORITHM")]
            )
            
            user_id =payload.get("user_id")

            stored_token = self.redis_client.get(f"access_token:{user_id}")

            if not stored_token or stored_token != token:
                raise HTTPException(status_code=401, detail="토큰이 만료되었거나 유효하지 않습니다.")

            if payload.get("type") != "access":
                raise HTTPException(status_code=401, detail="유효하지 않은 토큰 타입입니다.")
            

            user_data = {
                "user_id": payload["user_id"],
                "email": payload["email"],
                "is_authenticated": True
            }
            request.scope["user"] = user_data

            return await call_next(request)
            
        except JWTError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"유효하지 않은 토큰입니다: {str(e)}"}
            )
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": f"서버 내부 오류: {str(e)}"}
            )