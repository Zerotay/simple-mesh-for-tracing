from fastapi import FastAPI
from api.v1.routers import api_router
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Simple-Mesh",
    description="Forward traffics based on url, for tracing signal",
    version='1.0.0'
)
instrumenter = Instrumentator().instrument(app)
instrumenter.expose(app=app, include_in_schema=False)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port= 9090,
        host='0.0.0.0',
        reload=True,
    )

