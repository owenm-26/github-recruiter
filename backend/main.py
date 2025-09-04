from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user/{username}/exists")
async def user_exists(username:str):
    exists = False
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
    return {"message": message, "exists": exists}

@app.get('/user/{username}/repos')
def get_repos(username: str):
    repositories = requests.get(url=f"https://api.github.com/users/{username}/repos").json()

    return {"message": f"{username}'s repos", "repositories": repositories}

# @app.route('')
# def get_languages():
#     return []

# @app.route('')
# def get_packages_used():
#     return []
