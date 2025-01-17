from fastapi import FastAPI
from src.routes import proxy

app = FastAPI()

app.include_router(proxy.router)