from app.api.api_routes import router as routes_router
from app.api.routes.upload import router as upload_router
from fastapi import FastAPI

app = FastAPI(
    title="AI Based Product Answering Machine",
    version="2.0",
    description="An AI-powered product answering machine for processing queries and files",
)

app.include_router(routes_router)

app.include_router(upload_router, prefix="/files", tags=["upload"])
