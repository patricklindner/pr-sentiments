"""
This file contains the logic for enriching the pull request data in the dataset.
"""

from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader
import pymongo

DB_NAME = 'pull-requests-raw'
REPO_FILE_PATH = "../resources/project-list.txt"
RESOLUTION = 100


def main():
    database = get_database(DB_NAME)
    repo_reader = ProjectListReader(REPO_FILE_PATH)

    for _, repository in repo_reader:
        repository_collection = database[repository]
        enrich_repository_collection(repository_collection)


def enrich_repository_collection(repository_collection):
    user_contributions = dict()

    query = repository_collection.find({}).sort('_id', pymongo.DESCENDING)
    for row in query:
        if row['merged_at'] is None:
            continue
        update_contributions(user_contributions, row)


def update_contributions(user_contributions, row):
    author = row['user_id']
    user_contributions[author] = user_contributions.get(author, 0) + 1


if __name__ == '__main__':
    main()
