import requests
import base64
from fastapi import APIRouter, HTTPException
from pymongo.mongo_client import MongoClient
from db.mongodb import initialize_mongodb_python_client
from configs.logger import logger
from dotenv import load_dotenv
import os
import json
from services.users import process_repo_tree, merge_all_results


load_dotenv()
json_path = os.getenv("JSON_PATH")

with open(json_path, "r") as f:
    LANGUAGE_MAP = json.load(f)


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

    if len(users_repos) == 0:
        return {"message": "User has no repos in the MongoDB DB. Make sure you've written their repos to the DB before running this", "status": 404} 

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

@router.get("/{username}/packages")
def get_packages_used(username: str):
    results = {lang: set() for lang in LANGUAGE_MAP}

    # fetch repos for user
    try:
        repos_response = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"sort": "created", "direction": "desc", "per_page": 5}
        )
        repos_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching repositories for {username}: {str(e)}")

    repos_data = repos_response.json()
    if not isinstance(repos_data, list):
        raise HTTPException(status_code=404, detail=f"No repositories found for user {username}")

    for repo in repos_data:
        repo_name = repo.get("name")
        if not repo_name:
            continue

        # fetch repo tree
        try:
            repo_tree_resp = requests.get(
                f"https://api.github.com/repos/{username}/{repo_name}/git/trees/main?recursive=1",
                timeout=10,
            )
            repo_tree_resp.raise_for_status()
            repo_tree = repo_tree_resp.json()
        except requests.exceptions.RequestException as e:
            # skip this repo but continue with others
            continue

        # process repo files → dependencies
        try:
            repo_results = process_repo_tree(
                repo_tree,
                username,
                repo_name,
                LANGUAGE_MAP,
                lambda user, name, path: requests.get(
                    f"https://api.github.com/repos/{user}/{name}/contents/{path}", timeout=10
                ).json(),
            )
        except Exception as e:
            # if parsing fails, continue with other repos
            continue

        merge_all_results(results, repo_results)

    # convert sets → sorted lists
    results = {lang: sorted(list(pkgs)) for lang, pkgs in results.items() if pkgs}

    if not results:
        raise HTTPException(status_code=404, detail=f"No dependencies found for user {username}")

    return {"status": 200, "packages_by_language": results}