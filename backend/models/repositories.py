from pydantic import BaseModel, Field
import datetime
from typing import Optional, List

class Repository(BaseModel):
    id: int
    name: str 
    is_fork: bool = Field(alias="fork")
    repo_url: str = Field(alias="url")
    collaborators_url: str
    languages_url: str
    created_at: str
    updated_at: str
    stars: int = Field(alias="stargazers_count")
    forks_count: int
    primary_language: Optional[str] = Field(alias="language")
    topics: List[str] = []
    
class Config:
    populate_by_name = True

