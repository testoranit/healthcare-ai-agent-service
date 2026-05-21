# Healthcare AI Agent Service

Minimal FastAPI service for the Healthcare AI RAG Platform lab.

It exposes:

- `GET /health`
- `POST /ask`
- `POST /feedback`

The service supports two modes:

- `mock`: local safe response mode, no AWS call required
- `bedrock`: calls Amazon Bedrock Knowledge Bases through `bedrock-agent-runtime`

## Local run

```powershell
cd "C:\Users\SSSS\Documents\AI Lab2\healthcare-ai-agent-service"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:APP_MODE="mock"
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Test:

```powershell
Invoke-RestMethod http://localhost:8080/health
```

Ask:

```powershell
Invoke-RestMethod http://localhost:8080/ask `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"question":"What is the adverse drug reaction escalation process?","user_role":"nurse","department":"oncology"}'
```

## Bedrock mode

Use this after the Bedrock Knowledge Base and Guardrail are created.

```powershell
$env:APP_MODE="bedrock"
$env:AWS_REGION="ap-south-1"
$env:BEDROCK_KNOWLEDGE_BASE_ID="YOUR_KB_ID"
$env:BEDROCK_MODEL_ARN="arn:aws:bedrock:REGION::foundation-model/YOUR_MODEL"
$env:BEDROCK_GUARDRAIL_ID="YOUR_GUARDRAIL_ID"
$env:BEDROCK_GUARDRAIL_VERSION="DRAFT"
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Docker

```powershell
docker build -t healthcare-ai-agent:0.1.0 .
docker run --rm -p 8080:8080 -e APP_MODE=mock healthcare-ai-agent:0.1.0
```

## Safety rules

- Refuses diagnosis, dosage, emergency triage, and patient-specific medical advice.
- Requires grounded source context for real answers.
- Requires citations.
- Avoids logging raw PHI.
- Emits request IDs for audit correlation.
