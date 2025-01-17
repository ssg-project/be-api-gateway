from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SERVICE_ROUTES = {
    "user": os.getenv("TICKETING_USER_URL"),
    "ticketing": os.getenv("TICKETING_TICKETING_URL"),
    "event": os.getenv("TICKETING_EVENT_URL")
}

async def proxy_request(request: Request, service_url: str, path: str) -> StreamingResponse:
    headers = dict(request.headers)
    headers.pop("host", None)
    
    try:
        async with httpx.AsyncClient() as client:
            body = await request.body()
            
            response = await client.request(
                method=request.method,
                url=f"{service_url}{path}",
                headers=headers,
                content=body,
                params=request.query_params
            )
            
            return StreamingResponse(
                content=response.aiter_bytes(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_router(service: str, path: str, request: Request):
    service_url = SERVICE_ROUTES.get(service)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
        
    return await proxy_request(request, service_url, f"/{path}")
