import requests
from fastapi import APIRouter
from pymongo.mongo_client import MongoClient
from db.mongodb import initialize_mongodb_python_client
from configs.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])
mongo_client: MongoClient = initialize_mongodb_python_client(username=os.environ.get("MONGO_USER"), password=os.environ.get("MONGO_PASSWORD"))
db = mongo_client.get_database(name="CandidateData")
repo_collection = db.get_collection(name="Repositories")

headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

@router.get("/{username}/exists")
async def user_exists(username:str):
    exists = False
    status = 200
    try:
        response = requests.get(url=f"https://api.github.com/users/{username}", headers=headers).json()
        
        if response.get("login"):
            message = f"User {username} exists"
            exists = True
        else:
            message = f"User {username} does not exist"
    except Exception as e:
        message = f"Something went wrong. Got this exception: {e}"
        status = 500
    return {"message": message, "status": status, "exists": exists}

@router.get('/{username}/languages')
def get_languages(username:str):

    users_repos = list(repo_collection.find({"candidate_name": username, "is_fork": False}))
    language_volumes = {}

    logger.info(f'User Repos: {[repo.get("name") for repo in users_repos]}')

    for repo in users_repos:
        single_repo_languages_url = repo.get("languages_url")
        try:
            response = requests.get(url=single_repo_languages_url, headers=headers).json()
            # Add each language to the map
            for language in response:
                if language in language_volumes:
                    language_volumes[language] = {"lines_of_code": language_volumes[language].get("lines_of_code") + response[language],  "repo_ids": language_volumes[language].get("repo_ids") + [repo.get("id")]}
                else:
                    language_volumes[language] = {"lines_of_code": response[language], "repo_ids": [repo.get("id")]}
        except Exception as e:
            return {"message": f"Something went wrong. Got this exception: {e}", "status":500}
        
    return {"status": 200, "response": language_volumes}
    
@router.get('/{username}/packages')
def get_packages_used(username:str):
    return {"message": "hello"}