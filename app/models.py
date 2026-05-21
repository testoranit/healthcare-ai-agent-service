from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    user_role: str = Field(default="unknown", max_length=80)
    department: str = Field(default="unknown", max_length=80)


class Citation(BaseModel):
    document: str
    section: str | None = None
    s3_uri: str | None = None


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    guardrail_action: str
    request_id: str


class FeedbackRequest(BaseModel):
    request_id: str = Field(min_length=3, max_length=120)
    rating: int = Field(ge=-1, le=1)
    category: str = Field(default="general", max_length=80)
    comment: str | None = Field(default=None, max_length=1000)


class FeedbackResponse(BaseModel):
    status: str
    request_id: str
