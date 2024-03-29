"""
This file contains the logic for cleaning the data in the dataset.

The cleaning is done based on five criteria:
 1. Has the pull request been merged? No? Then remove!
 2. The pull request has a body text description.
 3. Has the pull request been closed in less than 5 minutes? Yes then it is
    likely reviewed offline or not at all. Remove.
 4. Are there comments? No? Then remove!
 5. Are is there interaction between author and reviewer(s) in the comments?
    Have both the author and the reviewer(s) made comments? No, then maybe it
    isn't a review. Remove.
"""

from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader
from src.helpers.loading_bar import print_loading_bar, print_finished_load_bar

from dateutil import parser
from pymongo.collection import Collection

DB_NAME_RAW = 'pull-requests-sentiment'
DB_NAME_CLEAN = 'pull-requests-sentiment-clean'
REPO_FILE_PATH = "./resources/project-list.txt"


def main():
    out_database = get_database(DB_NAME_CLEAN)
    in_database = get_database(DB_NAME_RAW)
    repository_reader = ProjectListReader(REPO_FILE_PATH)
    for _, repository in repository_reader:
        collection_in = in_database[repository]
        collection_out = out_database[repository]
        print(f"cleaning {repository}:")
        clean_project(collection_in, collection_out)
        print_finished_load_bar()


def is_dirty_row(row: dict):
    if not row['merged_at']:
        return True

    if not row['body']:
        return True

    created_time = parser.parse(row['created_at'])
    merged_time = parser.parse(row['merged_at'])
    if (merged_time - created_time).seconds < 300:
        return True

    if 'comments_participants' not in row.keys():
        return False

    if row.get('comments') == []:
        return True

    if 'author_comment_average' not in row.keys():
        return False

    if not row['author_comment_average'] or not row['review_comment_average']:
        return True

    return False


def clean_project(collection_in: Collection, collection_out: Collection):
    i, total = 0, collection_in.count_documents({})

    for pull_request_row in collection_in.find():
        print_loading_bar(i, total)
        i += 1

        if is_dirty_row(pull_request_row):
            continue

        collection_out.insert_one(pull_request_row)


if __name__ == '__main__':
    print("We are going to clean some data.")
    main()
