from models.repos import Repository
from datetime import datetime, timezone


def repository_parser(repo_objects: dict) -> list[Repository]:
    repositories = []
    for r in repo_objects:
        candidate_name =r.get("owner").get("login")
        created_at=convert_str_to_datetime(r.get("created_at"))
        updated_at=convert_str_to_datetime(r.get("updated_at"))
        repo = Repository(candidate_name=candidate_name,
                          created_date=created_at,
                        updated_date=updated_at,
                        **r)    
        repositories.append(repo)    
    return repositories

def convert_str_to_datetime(s:str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)