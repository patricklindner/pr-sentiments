from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader

from textblob import TextBlob
from pymongo.collection import Collection

DB_NAME = 'pull-requests-raw'
BAR_LENGTH = 50
REPO_FILE_PATH = "../resources/project-list.txt"


def main():
    database = get_database(DB_NAME)
    repo_reader = ProjectListReader(REPO_FILE_PATH)
    for _, repository in repo_reader:
        repository_collection = database[repository]
        print(f"Adding sentiments for {repository}")
        add_sentiment_data(repository_collection)


def print_loading_bar(i: int, total: int):
    done, left = i, total - i
    loading_bar = '.' * ((BAR_LENGTH * done + total - 1) // total)
    loading_bar += ' ' * ((BAR_LENGTH * left) // total)
    loading_bar += f"\t{i / total * 100:.2f}%"
    print(f"\r{loading_bar}", end='\n'*(i == total), flush=True)


def calculate_sentiment(pull_request: dict) -> dict:
    text = f"{pull_request['title']}\n{pull_request['body']}"
    textBlob = TextBlob(text)
    sentiment = textBlob.sentiment
    pull_request['sentiment'] = {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity
    }
    return pull_request


def add_sentiment_data(repository_collection: Collection):
    i, total = 0, repository_collection.count_documents({})

    for pull_request in repository_collection.find():
        repository_collection.replace_one(
            {'_id': pull_request["_id"]},
            calculate_sentiment(pull_request)
        )

        print_loading_bar(i, total)
        i += 1
    print_loading_bar(1, 1)


if __name__ == '__main__':
    main()
