from fastapi import FastAPI
from api.v1.routers import api_router
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

from core.config import settings
from core.logger import get_logger

app = FastAPI(
    title="Simple-Mesh",
    description="Forward traffics based on url, for tracing signal",
    version='1.0.0'
)
# Prometheus metric
instrumenter = Instrumentator().instrument(app)
instrumenter.expose(app=app, include_in_schema=False)
# Router Settings
app.include_router(api_router)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info(f"Turning up server... on {settings.ADDRESS}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        port= settings.PORT,
        host= str(settings.ADDRESS),
        reload=True,
    )

