import re

UNSAFE_PATTERNS = [
    r"\bdosage\b",
    r"\bdose\b",
    r"\bdiagnos(e|is|tic)\b",
    r"\bemergency\b",
    r"\btriage\b",
    r"\binsulin units\b",
    r"\bprescribe\b",
    r"\btreatment plan\b",
    r"\bignore (all )?previous instructions\b",
    r"\bsystem prompt\b",
]


def local_guardrail_action(question: str) -> str:
    normalized = question.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, normalized):
            return "BLOCKED_LOCAL_POLICY"
    return "NONE"


def safe_refusal() -> str:
    return (
        "I cannot provide diagnosis, dosage, emergency triage, or patient-specific "
        "medical advice. Please follow the approved clinical escalation process or "
        "contact a qualified healthcare professional."
    )
