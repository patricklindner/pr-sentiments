from src.util.GithubApiPageIterator import GithubApiPageIterator
from src.util.ProjectListReader import ProjectListReader
from src.util.mongo import get_database
from src.util.PullRequest import PullRequest
from pymongo.errors import DuplicateKeyError

BASE_URL = "https://api.github.com/repos/{owner}/{repo}/pulls"
DB_NAME = 'pull-requests-raw'
REPO_FILE_PATH = "../resources/project-list.txt"


def main():
    reader = ProjectListReader(REPO_FILE_PATH)
    db_raw = get_database(DB_NAME)
    for owner, repo in reader:
        collection = db_raw[repo]
        pull_repository(owner, repo, collection)


def pull_repository(owner, repo, collection):
    print("pulling repo", repo)

    page_iterator = GithubApiPageIterator(
        BASE_URL.format(owner=owner, repo=repo),
        params={"state": "closed", "per_page": 100}
    )

    for page in page_iterator:
        for pr_json in page:
            pull_request = PullRequest(pr_json)
            try:
                collection.insert_one(pull_request.to_json())
                print('.', end='', flush=True)
            except DuplicateKeyError:
                print('D', end='', flush=True)
                if not page_iterator.jumped:
                    page_iterator.jump(collection.count_documents({}))
            except Exception as e:
                print("Unexepected Error!:", e)
                print("Skipping pull request with id", pr_json["id"])
        print()
        page_iterator.print_progress()


if __name__ == '__main__':
    main()
