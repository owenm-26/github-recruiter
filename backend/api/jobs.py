from fastapi import APIRouter, HTTPException
from services.jobs import parse_job_description
from services.exceptions import JobParseError, AgentInitError, LLMCallError
from pymongo.mongo_client import MongoClient
from db.mongodb import initialize_mongodb_python_client
import os
from dotenv import load_dotenv
from models.jobs import Job
import datetime
load_dotenv()

router = APIRouter(prefix="/jobs", tags=["jobs"])

mongo_client: MongoClient = initialize_mongodb_python_client(username=os.environ.get("MONGO_USER"), password=os.environ.get("MONGO_PASSWORD"))
db = mongo_client.get_database(name="JobData")
job_description_collection = db.get_collection(name="JobDescriptions")

@router.post("/parse-job-description")
def parse_job(job_description: str, position_name:str, recruiter_id: int):
    try:
        response = parse_job_description(job_description)
        parsed_job = response.output
        # write to DB
        new_job = Job(position_name=position_name, recruiter_id=recruiter_id, candidates_reviewed_ids=[], languages=parsed_job, date_parsed=datetime.datetime.now())
        job_description_collection.insert_one(new_job.model_dump())
        return {"message": f"{position_name} from recruiter {recruiter_id} parsed and written to DB", "job": new_job, "status": 200}
    except JobParseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (AgentInitError, LLMCallError):
        raise HTTPException(status_code=502, detail="Upstream model error")