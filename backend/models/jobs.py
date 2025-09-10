from pydantic import BaseModel, Field
import datetime
from typing import List

class Library(BaseModel):
    name: str
    identifier: str = Field(..., description="The abbreviated name of the package that would be present in dependency files")

class Language(BaseModel):
    name: str
    priority: int = Field(..., ge=1, le=5, description="Priority between 1 and 5")
    libraries: List[Library] = Field(..., description="ML libraries or web dev frameworks etc.")

class LanguagesList(BaseModel):
    languages: List[Language]

class Job(BaseModel):
    id: int
    recruiter_id: int
    candidates_reviewed_ids: List[int]
    languages: LanguagesList
    date_parsed: datetime.datetime