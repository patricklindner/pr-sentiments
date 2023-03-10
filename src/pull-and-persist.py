from src.util.GithubApiPageIterator import GithubApiPageIterator
from src.util.ProjectListReader import ProjectListReader
from src.util.mongo import get_database
from pymongo.errors import DuplicateKeyError

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
    # iterate over all pages
    for page in pageIterator:
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
                print('.', end='')
            except DuplicateKeyError:
                print('D', end='')
                if not pageIterator.jumped:
                    pageIterator.jump(collection.count_documents({}))
            except Exception as e:
                print("Unexepected Error!:", e)
                print("Skipping pull request with id", pr["id"])
        print()
        pageIterator.print_progress()
