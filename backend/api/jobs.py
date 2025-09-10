from fastapi import APIRouter, HTTPException
from services.jobs import parse_job_description
from services.exceptions import JobParseError, AgentInitError, LLMCallError


router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/parse-job-description")
def parse_job(job_description: str):
    try:
        parsed = parse_job_description(job_description)
        return {"message": "Job description parsed", "job": parsed, "status": 200}
    except JobParseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (AgentInitError, LLMCallError):
        raise HTTPException(status_code=502, detail="Upstream model error")