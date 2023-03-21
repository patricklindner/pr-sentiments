import requests
from src.helpers.token import get_token_header
from pymongo.collection import Collection
from time import sleep


def enrich_user_data(data: dict, collection: Collection):
    """
    This function adds information about the author of a pull request.
    Namely:
        - Number of pull requests this user has made in this repo (TODO)
        - Number of followers of the user (TODO)

    Args:
        data (dict): The pull request data so far
    """
    data['user'] = None
    pass


def enrich_pr_data(data: dict, pull_request: dict):
    """
    This function adds information about the pull request itself.
    Namely:
        - The number of lines added
        - The number of lines removed
        - The number of commits
        - The number of files changed
        - The number of requested reviewers

    Args:
        data (dict): The pull request data so far
    """
    data['pull_request'] = dict()
    data['pull_request']['added'] = pull_request['additions']
    data['pull_request']['removed'] = pull_request['deletions']
    requested_reviewers = pull_request['requested_reviewers']
    data['pull_request']['request_reviewers'] = len(requested_reviewers)
    data['pull_request']['commits'] = pull_request['commits']
    data['pull_request']['changed_files'] = pull_request['changed_files']


def enrich_project_data(data: dict, project: dict):
    """
    This function adds information about the project of the pull request.
    Namely:
        - The number of watchers
        - The size of the project
        - The age of the project at the time of the pull request
        - The language of the code

    Args:
        data (dict): The pull request data so far
    """
    data['project'] = dict()
    data['project']['name'] = project['name']
    data['project']['watchers'] = project['watchers']
    data['project']['created_at'] = project['created_at']
    data['project']['size'] = project['size']
    data['project']['language'] = project['language']


def enrich_comments_data(data: dict, comments: dict):
    """
    This function adds information about the comments for a pull request.
    Namely:
        - The number of comments
        - The number of unique commenters
        - The text of the comments
        - The user ids of the comments

    Args:
        data (dict): The pull request data so far
    """
    data['comments_count'] = len(comments)
    participants = set([c['user']['id'] for c in comments if c['user']])
    data['comments_participants'] = len(participants)
    data['comments'] = [
        {'user_id': comment['user']['id'], 'text': comment['body']}
        for comment in comments if comment['user']
    ]


def enrich_based_on_pull_request_api(data, base_url):
    if data.get('pull_request') and data.get('project'):
        return

    headers = get_token_header()
    pull_url = base_url + f"/{data['number']}"
    response_pull_request = requests.get(pull_url, headers=headers)
    sleep(2)  # Lets not flood the git API

    if response_pull_request.status_code == 200:
        pull_request = response_pull_request.json()
        enrich_pr_data(data, pull_request)
        enrich_project_data(data, pull_request['base']['repo'])
    else:
        print(response_pull_request.status_code)
        print(response_pull_request.json())


def enrich_based_on_comment_api(data, base_url):
    if data.get('comments') or data.get('comments') == []:
        return

    headers = get_token_header()
    comments_url = base_url + f"/{data['number']}/comments"
    response_comments = requests.get(comments_url, headers=headers)
    sleep(2)  # Lets not flood the git API

    if response_comments.status_code == 200:
        comments = response_comments.json()
        enrich_comments_data(data, comments)
    else:
        print(response_comments.status_code)
        print(response_comments.json())


def enrich_based_on_repository_collection(data, collection: Collection):
    if data.get('user'):
        return

    enrich_user_data(data, collection)


def enrich_pull_request(data: dict, collection: Collection, base_url: str):
    enrich_based_on_pull_request_api(data, base_url)
    enrich_based_on_comment_api(data, base_url)
    enrich_based_on_repository_collection(data, collection)
    return data
