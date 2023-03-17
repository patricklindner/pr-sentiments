class PullRequest():
    """
    This class holds the data for pull requests.
    """

    def __init__(self, base_json: dict) -> None:
        self.me_json = base_json

    def to_json(self) -> dict:
        return {
            "_id": self.me_json["id"],
            "title": self.me_json["title"],
            "body": self.me_json["body"],
            "created_at": self.me_json["created_at"],
            "closed_at": self.me_json["closed_at"],
            "merged_at": self.me_json["merged_at"],
            "user_id": self.me_json["user"]["id"],
            "url": self.me_json['url'],
            "comments_url": self.me_json['comments_url'],
            "user_url": self.me_json['user']['url']
        }
