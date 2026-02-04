from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    message: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en", pattern="^(en|fr)$")


class ChatResponse(BaseModel):
    response: str
    language: str
    timestamp: datetime


class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    context: str = Field(default="")
    language: str = Field(default="en")


class MedicalAnalysis(BaseModel):
    summary: str
    key_findings: List[str]
    recommendations: List[str]
    next_steps: List[str]


class AnalysisResponse(BaseModel):
    summary: str
    key_findings: List[str]
    recommendations: List[str]
    next_steps: List[str]
    disclaimer: str
    language: str
    timestamp: datetime


class ImageAnalysisResponse(BaseModel):
    extracted_text: str
    analysis: AnalysisResponse


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=200)
    max_results: int = Field(default=5, ge=1, le=10)
    language: str = Field(default="en")


class ResearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float


class ResearchResponse(BaseModel):
    query: str
    results: List[ResearchResult]
    summary: str
    timestamp: datetime
