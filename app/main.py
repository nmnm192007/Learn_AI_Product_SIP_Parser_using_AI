from app.api.routes.upload import router as upload_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(upload_router)
