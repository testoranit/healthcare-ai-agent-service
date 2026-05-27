##testing
import logging
from uuid import uuid4

from fastapi import FastAPI

from app.bedrock_client import BedrockRagClient
from app.config import Settings, get_settings
from app.logging_config import configure_logging
from app.models import AskRequest, AskResponse, Citation, FeedbackRequest, FeedbackResponse
from app.safety import local_guardrail_action, safe_refusal

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("healthcare-ai-agent")

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "mode": settings.app_mode,
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    request_id = str(uuid4())
    guardrail_action = local_guardrail_action(request.question)

    if guardrail_action != "NONE":
        logger.info(
            "request blocked by local safety policy",
            extra={"request_id": request_id},
        )
        return AskResponse(
            answer=safe_refusal(),
            citations=[],
            guardrail_action=guardrail_action,
            request_id=request_id,
        )

    if settings.app_mode == "bedrock":
        answer, citations, guardrail_action = _ask_bedrock(settings, request)
    else:
        answer, citations, guardrail_action = _ask_mock(request)

    if not citations and guardrail_action == "NONE":
        answer = "I could not find approved policy evidence for this question."
        guardrail_action = "NO_GROUNDED_CONTEXT"

    logger.info(
        "request completed",
        extra={"request_id": request_id},
    )

    return AskResponse(
        answer=answer,
        citations=citations,
        guardrail_action=guardrail_action,
        request_id=request_id,
    )


@app.post("/feedback", response_model=FeedbackResponse)
def feedback(request: FeedbackRequest) -> FeedbackResponse:
    logger.info(
        "feedback received",
        extra={"request_id": request.request_id},
    )
    return FeedbackResponse(status="accepted", request_id=request.request_id)


def _ask_bedrock(settings: Settings, request: AskRequest) -> tuple[str, list[Citation], str]:
    client = BedrockRagClient(settings)
    return client.ask(
        question=request.question,
        user_role=request.user_role,
        department=request.department,
    )


def _ask_mock(request: AskRequest) -> tuple[str, list[Citation], str]:
    return (
        "Mock response: follow the approved healthcare SOP and escalate according to the documented process.",
        [
            Citation(
                document="ADR_Escalation_SOP.pdf",
                section="4.2",
                s3_uri="s3://synthetic-healthcare-rag-docs/sops/ADR_Escalation_SOP.pdf",
            )
        ],
        "NONE",
    )
