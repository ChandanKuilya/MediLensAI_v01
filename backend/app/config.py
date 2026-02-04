import os
from pydantic_settings import BaseSettings
from pydantic import Field
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import lru_cache


class Settings(BaseSettings):
    google_api_key: str = Field(..., description="Google Gemini API key")
    tavily_api_key: str = Field(..., description="Tavily API key")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    cors_origins: str = Field(default="http://localhost:3000")
    gemini_model: str = Field(default="gemini-2.0-flash-exp")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=100, le=8192)
    max_file_size: int = Field(default=10 * 1024 * 1024)

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore" 

    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()


@lru_cache()
def load_google_llm():
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=settings.temperature,
        max_output_tokens=settings.max_tokens,
        convert_system_message_to_human=True
    )


@lru_cache()
def load_google_vision_llm():
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0.5,
        max_output_tokens=settings.max_tokens,
        convert_system_message_to_human=True
    )
