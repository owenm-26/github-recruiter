from models.repositories import Repository
def repository_parser(repo_objects: dict) -> list[Repository]:
    repositories = [Repository(**r) for r in repo_objects] 
    return repositories
