from fastapi import FastAPI
from api import api_router

app = FastAPI(title="My Project API")

# Mount all routes
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "This is the backend for GitHub Recruiter. Use `/docs` to see the endpoints"}