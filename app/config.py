from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "healthcare-ai-agent"
    app_mode: Literal["mock", "bedrock"] = "mock"
    aws_region: str = "ap-south-1"
    bedrock_knowledge_base_id: str | None = None
    bedrock_model_arn: str | None = None
    bedrock_guardrail_id: str | None = None
    bedrock_guardrail_version: str = "DRAFT"
    retrieval_results: int = 5
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
