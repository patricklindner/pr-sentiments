class PullRequest():
    """
    This class holds the data for pull requests.
    It also preforms additional requests to gather additional information.
    """

    def __init__(self, base_json: dict) -> None:
        self.response_json = base_json

    def to_mongo_json(self) -> dict:
        return {
            "_id": self.response_json["id"],
            "title": self.response_json["title"],
            "body": self.response_json["body"],
            "created_at": self.response_json["created_at"],
            "closed_at": self.response_json["closed_at"],
            "merged_at": self.response_json["merged_at"],
            "user_id": self.response_json["user"]["id"],
            # we can better not persist the urls as string for the sake of disc space, They can be build easily using the pull id
        }

    @staticmethod
    def __get_token_header():
        with open("../resources/token.txt", "r") as token_file:
            token = token_file.readline()
            if token != "":
                return {"Authorization": "Bearer " + token}
        raise AssertionError("Token file could not be read")
