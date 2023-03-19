import logging
import threading

from rich.progress import Progress

from util.GithubApiPageIterator import GithubApiPageIterator
from util.ProjectListReader import ProjectListReader
from util.PullRequest import PullRequest
from util.mongo import get_database

base_url = "https://api.github.com/repos/{owner}/{repo}/pulls"


def pull_and_persist(owner, repo, progress_bar):
    logging.info(f"pulling repo {repo}")
    collection = db_raw[repo]

    page_iterator = iter(GithubApiPageIterator(
        f"{owner}/{repo}",
        base_url.replace("{owner}", owner).replace("{repo}", repo),
        params={"state": "closed", "per_page": 100}
    ))

    progress_task = progress_bar.add_task(f"{owner}/{repo}", total=len(page_iterator))
    # bar = tqdm(page_iterator, desc=f"{repo.ljust(25)}", ncols=100, leave=False)
    # iterate over all pages
    # do not use a for loop since it would call the __iter__ function again,
    # which results in fetching the initial request again
    while True:
        try:
            page = next(page_iterator)
            # iterate over all elements of page
            for pr_json in page:
                pull_request = PullRequest(pr_json)
                try:
                    collection.insert_one(pull_request.to_mongo_json())
                except Exception as e:
                    logging.warning(f"Unexepected Error!: {e}")

            progress_bar.update(progress_task, advance=1)
        except StopIteration:
            break


if __name__ == '__main__':

    logging.basicConfig(
        filename="../logs/warn.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,

    )
    reader = ProjectListReader("../resources/project-list.txt")
    db_raw = get_database("pull-requests-raw")

    with Progress() as progress_bar:
        threads = list()
        # pull_and_persist("ant-design", "ant-design", 12)
        for owner, repo in reader:
            t = threading.Thread(target=pull_and_persist, args=(owner, repo, progress_bar), name=repo)
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()
