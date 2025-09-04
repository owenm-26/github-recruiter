from fastapi import FastAPI
import typing


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/user/{username}/repos')
def get_repos(username: str) -> typing.Dict:
    return {"message": f"{username}'s repos"}

# @app.route('')
# def get_languages():
#     return []

# @app.route('')
# def get_packages_used():
#     return []
