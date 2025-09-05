from fastapi import FastAPI, Body
import requests
import json
from pymongo.mongo_client import MongoClient
from db.mongodb import initialize_mongodb_python_client
from models.repositories import Repository
from services.repositories import repository_parser
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

mongo_client: MongoClient = initialize_mongodb_python_client(username=os.environ.get("MONGO_USER"), password=os.environ.get("MONGO_PASSWORD"))
db = mongo_client.get_database(name="CandidateData")
repo_collection = db.get_collection(name="Repositories")

@app.get("/")
async def root():
    return {"message": "This is the backend for GitHub Recruiter. Use `/docs` to see the endpoints"}

@app.get("/user/{username}/exists")
async def user_exists(username:str):
    exists = False
    status = 200
    try:
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }
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

@app.get('/user/{username}/repos/read')
def get_repos(username: str):
    repositories = requests.get(url=f"https://api.github.com/users/{username}/repos").json()

    transformed_repos: list[Repository] = repository_parser(repo_objects=repositories)

    return {"message": f"{username}'s repos", "status": 200, "repositories": transformed_repos}

@app.post('/user/{username}/repos/write')
def write_repos(username: str, repositories: list[Repository]= Body(...)):
    assert repositories is not None
    try: 
        repo_collection.insert_many([repo.model_dump() for repo in repositories])
    except Exception as e:
        return {'message': f'Error during write: {e}', 'status': 500} 

    return {"message": f"Wrote {username}'s repos to DB", "status": 200}

@app.delete('/user/{username}/repos/delete')
def delete_repos(username: str):
    try:
        repo_collection.delete_many({"candidate_name": username})
    except Exception as e:
        return {'message': f'Error during deletion: {e}', 'status': 500} 
    return {"message": f"Deleted {username}'s repos from DB", "status": 200}

@app.get('/user/{username}/languages')
def get_languages(username:str):

    return {"message": "hello"}

@app.get('/user/{username}/packages')
def get_packages_used(username:str):
    return {"message": "hello"}


