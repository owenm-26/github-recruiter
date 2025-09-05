import requests
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}/exists")
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

@router.get('/{username}/languages')
def get_languages(username:str):

    return {"message": "hello"}

@router.get('/{username}/packages')
def get_packages_used(username:str):
    return {"message": "hello"}