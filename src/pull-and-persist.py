from src.util.GithubApiPageIterator import GithubApiPageIterator
from src.util.ProjectListReader import ProjectListReader
from src.util.mongo import get_database

base_url = "https://api.github.com"
pull_request_url = base_url + "/repos/{owner}/{repo}/pulls"

reader = ProjectListReader("../resources/project-list.txt")

db_raw = get_database("pull-requests-raw")

for owner, repo in reader:
    print("pulling repo", repo)

    pageIterator = GithubApiPageIterator(
        pull_request_url.replace("{owner}", owner).replace("{repo}", repo),
        params={"state": "closed", "per_page": 100}
    )

    collection = db_raw[repo]
    page_number = 0
    # iterate over all pages
    for page in pageIterator:
        print("progress {:.2f}%".format((page_number / pageIterator.total_pages * 100)))
        page_number += 1
        # iterate over all elements of page
        for pr in page:
            item = {
                "_id": pr["id"],
                "title": pr["title"],
                "body": pr["body"],
                "created_at": pr["created_at"],
                "closed_at": pr["closed_at"],
                "merged_at": pr["merged_at"],
                "user_id": pr["user"]["id"]
            }
            try:
                collection.insert_one(item)
            except:
                print("Skipping pull request with id", pr["id"])
