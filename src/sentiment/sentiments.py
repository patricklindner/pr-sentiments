from textblob import TextBlob


def textblog_sentiment_json(text: str) -> dict:
    if not text:
        return None

    textBolb = TextBlob(text)
    sentiment = textBolb.sentiment
    return {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity
    }


def get_sentiments(pull_request: dict) -> dict:
    sentiments = pull_request
    add_post_sentiment(sentiments)
    add_comments_sentiments(sentiments)
    return sentiments


def add_post_sentiment(pull_request: dict):
    pull_request['title'] = textblog_sentiment_json(pull_request['title'])
    pull_request['body'] = textblog_sentiment_json(pull_request['body'])


def add_comments_sentiments(pull_request: dict):
    comments = pull_request['comments']
    if not comments:
        return

    for comment in comments:
        comment['text'] = textblog_sentiment_json(comment['text'])

    add_comment_averages(pull_request, comments)


def add_comment_averages(pull_request: dict, comments: list):
    author = pull_request['user_id']
    author_comments = [
        comment for comment in comments
        if comment['user_id'] == author
    ]
    review_comments = [
        comment for comment in comments
        if comment['user_id'] != author
    ]

    pull_request['all_comment_average'] = average_sentiment(comments)
    pull_request['author_comment_average'] = average_sentiment(author_comments)
    pull_request['review_comment_average'] = average_sentiment(review_comments)


def average_sentiment(comments: list):
    """This function gets the average sentiment of a list of comments."""
    if not comments:
        return None

    polarities = [comment['text']['polarity'] for comment in comments]
    subjectivities = [comment['text']['subjectivity'] for comment in comments]

    return {
        'polarity': sum(polarities) / len(polarities),
        'subjectivity': sum(subjectivities) / len(subjectivities)
    }
