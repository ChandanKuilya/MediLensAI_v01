from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import health, analysis, research

app = FastAPI(
    title="MediCare AI Backend",
    description="Medical AI Assistant API for Cameroon - Powered by LangChain",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

#resoures to reference: https://dev.to/fonyuygita/building-a-production-ready-medical-ai-assistant-with-python-fastapi-tavili-gemini-langchain-5693

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(research.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to MediCare AI Backend",
        "version": "2.0.0",
        "powered_by": "LangChain + Google Gemini",
        "docs": "/docs",
        "status": "running"
    }
