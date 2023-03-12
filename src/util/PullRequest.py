class PullRequest():
    """
    This class holds the data for pull requests.
    It also preforms additional requests to gather additional information.
    """

    def __init__(self, base_json: dict) -> None:
        self.response_json = base_json

    def _get_line_count(self):
        pass

    def _get_reviewers(self):
        pass

    def _get_comments(self):
        pass

    def to_json(self) -> dict:
        return {
            "_id": self.response_json["id"],
            "title": self.response_json["title"],
            "body": self.response_json["body"],
            "created_at": self.response_json["created_at"],
            "closed_at": self.response_json["closed_at"],
            "merged_at": self.response_json["merged_at"],
            "user_id": self.response_json["user"]["id"]
        }
