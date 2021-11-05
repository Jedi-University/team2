def mapping_repo(repo: dict) -> dict:
    return {
        "id": repo["id"],
        "org_name": repo["owner"]["login"],
        "repo_name": repo["name"],
        "stars_count": repo["stargazers_count"],
    }
