from settings.gh_token import gh_token as token

base_uri = "https://api.github.com"
org_uri = "/organizations"
orgs_list =[]
repo_list = []
headers = {'Accept':"application/vnd.github+json", "authorization": f"Bearer {token}"}