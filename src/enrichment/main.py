"""
This file contains the logic for enriching the pull request data in the
dataset.
"""

from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader
from src.helpers.token import sleeper
from src.helpers.loading_bar import print_loading_bar, print_finished_load_bar
from src.enrichment.enricher import enrich_pull_request

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pymongo.collection import Collection

DB_NAME = 'pull-requests-clean'
REPO_FILE_PATH = "./resources/project-list.txt"
BASE_URL = 'https://api.github.com/repos/{author}/{repository}/pulls'
RESOLUTION = 100
BATCH_SIZE = 20
MAX_WORKERS = 20
REQUESTS_PER_PR = 2


def main():
    database = get_database(DB_NAME)
    repo_reader = ProjectListReader(REPO_FILE_PATH)

    for author, repository in repo_reader:
        repository_collection = database[repository]
        repository_url = BASE_URL.format(author=author, repository=repository)
        print(f'enriching {repository}:')
        enrich_repository_collection(repository_collection, repository_url)


@sleeper(number_of_requests=(REQUESTS_PER_PR * BATCH_SIZE))
def async_batch(
    batch: list,
    repository_collection: Collection,
    repository_url: str
):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        enrich_batch(batch, repository_collection, repository_url)
    )


async def enrich_batch(
    batch: list,
    repository_collection: Collection,
    repository_url: str
):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                enrich_pull_request,
                batch[i],
                repository_collection,
                repository_url
            ) for i in range(BATCH_SIZE)
        ]

        for enriched_pull_request in await asyncio.gather(*futures):
            update_pull_request(enriched_pull_request, repository_collection)


def update_pull_request(pull_request: dict, repository_collection: Collection):
    pull_request_id = pull_request['_id']
    repository_collection.replace_one(
        {'_id': pull_request_id},
        pull_request
    )


def enrich_repository_collection(
    repository_collection: Collection,
    repository_url: str
):
    size = repository_collection.count_documents({})
    for i in range(0, size, BATCH_SIZE):
        print_loading_bar(i, size)
        batch_query = repository_collection.find({}).skip(i).limit(size)
        batch = list(batch_query)
        async_batch(batch, repository_collection, repository_url)
    print_finished_load_bar()


if __name__ == '__main__':
    print("Lets enrich some data!")
    main()
