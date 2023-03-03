from src.util.mongo import get_database
from textblob import TextBlob

DB_NAME = 'pull-requests-raw'
REPO = 'tensorflow'

def main():
    database = get_database(DB_NAME)
    repo_collection = database[REPO]


    for pull_request in repo_collection.find():
        text = f"{pull_request['title']}\n{pull_request['title']}"
        textBlob = TextBlob(text)
        sentiment = textBlob.sentiment
        pull_request['sentiment'] = {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        }
        print(pull_request)
        repo_collection.replace_one({'_id': pull_request["_id"]}, pull_request)


if __name__ == '__main__':
    main()
