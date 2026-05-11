from app.api.routes import router
from fastapi import FastAPI

app = FastAPI(
    title="AI based SIP call flow analyser",
    description="RAG-based system to analyze SIP call flows and failures",
    version="1.0.0",
)

app.include_router(router)
