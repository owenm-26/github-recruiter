from pydantic import BaseModel, Field
import datetime
from typing import Optional, List

class Repository(BaseModel):
    candidate_name: Optional[str] = None
    name: str 
    is_fork: bool = Field(alias="fork")
    repo_url: str = Field(alias="url")
    collaborators_url: str
    languages_url: str
    created_date: datetime.datetime = None
    updated_date: datetime.datetime = None
    stars: int = Field(alias="stargazers_count")
    forks_count: int
    primary_language: Optional[str] = Field(alias="language")
    topics: List[str] = []
class Config:
    populate_by_name = True

