class PullRequest():
    """
    This class holds the data for pull requests.
    It also preforms additional requests to gather additional information.
    """

    def __init__(self, base_json: dict) -> None:
        self.response_json = base_json
        # self.my_json = self._request_self()

    # def _request_self(self):
    #     links = self.response_json['_links']
    #     response_self = requests.get(
    #         links['self']['href'],
    #         headers=self.__get_token_header()
    #     )
    #
    #     if response_self.status_code != 200:
    #         print(response_self.text)
    #         sleep(2)
    #         return self._request_self()
    #     return response_self.json()

    # def _request_comments(self):
    #     links = self.response_json['_links']
    #     response_comments = requests.get(
    #         links['comments']['href'],
    #         headers=self.__get_token_header()
    #     )
    #
    #     if response_comments.status_code != 200:
    #         print(response_comments.text)
    #         sleep(2)
    #         return self._request_comments()
    #     return response_comments.json()
    #
    # def comment_to_json(self, comment):
    #     return {
    #         "text": comment['body'],
    #         'user_id': comment['user']['id']
    #     }

    def to_mongo_json(self) -> dict:
        return {
            "_id": self.response_json["id"],
            "title": self.response_json["title"],
            "body": self.response_json["body"],
            "created_at": self.response_json["created_at"],
            "closed_at": self.response_json["closed_at"],
            "merged_at": self.response_json["merged_at"],
            "user_id": self.response_json["user"]["id"],
            # "additions": self.my_json["additions"],
            # "deletions": self.my_json["deletions"],
            # "changed_files": self.my_json["changed_files"],
            # we can better not persist the urls as string for the sake of disc space, They can be build easily using the pull id
        }

    @staticmethod
    def __get_token_header():
        with open("../resources/token.txt", "r") as token_file:
            token = token_file.readline()
            if token != "":
                return {"Authorization": "Bearer " + token}
        raise AssertionError("Token file could not be read")
