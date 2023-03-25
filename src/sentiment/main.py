from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader
from src.helpers.loading_bar import (
    print_finished_load_bar,
    print_loading_bar,
    print_empty_load_bar
)
from src.sentiment.sentiments import get_sentiments

from pymongo.collection import Collection

DB_CLEAN = 'pull-requests-clean'
DB_SENTIMENT = 'pull-requests-sentiment'
REPO_FILE_PATH = './resources/project-list.txt'


def main():
    database_in = get_database(DB_CLEAN)
    database_out = get_database(DB_SENTIMENT)
    repo_reader = ProjectListReader(REPO_FILE_PATH)
    for _, repository in repo_reader:
        collection_in = database_in[repository]
        collection_out = database_out[repository]
        print(f"Computing sentiments for {repository}")
        compute_sentiment_data(collection_in, collection_out)


def compute_sentiment_data(
    collection_in: Collection,
    collection_out: Collection
):
    i, total = 0, collection_in.count_documents({})
    print_empty_load_bar()

    for pull_request in collection_in.find():
        sentiments = get_sentiments(pull_request)
        collection_out.insert_one(sentiments)
        i += 1
        print_loading_bar(i, total)

    print_finished_load_bar()


if __name__ == '__main__':
    print("Lets get sentimental:")
    main()
