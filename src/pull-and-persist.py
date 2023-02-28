from src.util.ProjectListReader import ProjectListReader
import requests

base_url = "https://api.github.com"
pull_request_url = base_url + "/repos/{owner}/{repo}/pulls"

reader = ProjectListReader("../resources/project-list.txt")

for owner, repo in reader:
    print(owner, repo)
    resp = requests.get(pull_request_url.replace("{owner}", owner).replace("{repo}", repo))
    print(resp.url)
    print(resp.json())
