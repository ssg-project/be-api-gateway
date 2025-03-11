from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import proxy
from src.middleware.auth import AuthMiddleware
import uvicorn
import logging
from prometheus_fastapi_instrumentator import Instrumentator

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

app.include_router(proxy.router)

# Prometheus 모니터링 활성화
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)