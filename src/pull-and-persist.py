import threading
import logging

from util.GithubApiPageIterator import GithubApiPageIterator
from util.ProjectListReader import ProjectListReader
from util.PullRequest import PullRequest
from util.mongo import get_database

from tqdm import tqdm

base_url = "https://api.github.com/repos/{owner}/{repo}/pulls"


def pull_and_persist(owner, repo, index):
    logging.info(f"pulling repo {repo}")

    page_iterator = iter(GithubApiPageIterator(
        f"{owner}/{repo}",
        base_url.replace("{owner}", owner).replace("{repo}", repo),
        params={"state": "open", "per_page": 100}
    ))

    collection = db_raw[repo]
    it = tqdm(page_iterator, desc=repo, position=index)
    # iterate over all pages
    for page in it:
        # iterate over all elements of page
        for pr_json in page:
            pull_request = PullRequest(pr_json)
            try:
                collection.insert_one(pull_request.to_mongo_json())
            #     print('.', end='', flush=True)
            # except DuplicateKeyError:
            #     print('D', end='', flush=True)
            #     if not page_iterator.jumped:
            #         page_iterator.jump(collection.count_documents({}))
            except Exception as e:
                logging.warning(f"Unexepected Error!: {e}")
                logging.warning(f"Skipping pull request with id {pr_json['id']}")


if __name__ == '__main__':

    logging.basicConfig(filename="../logs/warn.log")
    # logging.basicConfig(level=logging.INFO)
    reader = ProjectListReader("../resources/project-list.txt")
    db_raw = get_database("pull-requests-raw")

    pull_and_persist("opencv", "opencv", 0)
    # for i, (owner, repo) in enumerate(reader):
    #     t = threading.Thread(target=pull_and_persist, args=(owner, repo, i), name=repo)
    #     t.start()
