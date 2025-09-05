from fastapi import APIRouter, Body
import requests
from pymongo.mongo_client import MongoClient
from db.mongodb import initialize_mongodb_python_client
from models.repositories import Repository
from services.repositories import repository_parser
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter(prefix="/repos", tags=["repos"])

mongo_client: MongoClient = initialize_mongodb_python_client(username=os.environ.get("MONGO_USER"), password=os.environ.get("MONGO_PASSWORD"))
db = mongo_client.get_database(name="CandidateData")
repo_collection = db.get_collection(name="Repositories")

@router.get('/{username}/read')
def get_repos(username: str):
    repositories = requests.get(url=f"https://api.github.com/users/{username}/repos").json()

    transformed_repos: list[Repository] = repository_parser(repo_objects=repositories)

    return {"message": f"{username}'s repos", "status": 200, "repositories": transformed_repos}

@router.post('/{username}/write')
def write_repos(username: str, repositories: list[Repository]= Body(...)):
    assert repositories is not None
    try: 
        repo_collection.insert_many([repo.model_dump() for repo in repositories])
    except Exception as e:
        return {'message': f'Error during write: {e}', 'status': 500} 

    return {"message": f"Wrote {username}'s repos to DB", "status": 200}

@router.delete('/{username}/delete')
def delete_repos(username: str):
    try:
        repo_collection.delete_many({"candidate_name": username})
    except Exception as e:
        return {'message': f'Error during deletion: {e}', 'status': 500} 
    return {"message": f"Deleted {username}'s repos from DB", "status": 200}

