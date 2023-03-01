import re

import requests


class GithubApiPageIterator:

    def __init__(self, url, params=None):
        self.start_url = url
        self.params = params
        self.token = self.__get_token()
        resp = requests.get(
            url=url,
            params=params,
            headers={"Authorization": "Bearer " + self.token}
        )
        self.total_pages = int(self.__number_of_pages(resp.headers.get("link")))

    def __iter__(self):
        self.next_url = self.start_url
        self.first_request = True
        return self

    def __next__(self):
        if self.next_url is None:
            raise StopIteration
        else:
            resp = requests.get(
                url=self.next_url,
                params=self.params if self.first_request else None,
                headers={"Authorization": "Bearer " + self.__get_token()}
            )
            self.first_request = False
            if resp.status_code >= 200:
                print("Fetched from:", resp.url)
                self.next_url = self.__extract_next_link(resp.headers.get("link"))
                return resp.json()
            else:
                print("Something went wrong", resp)

    @staticmethod
    def __extract_next_link(link_string):
        match = re.search('(?<=<)([\\S]*)(?=>; rel="next")', link_string)
        if match:
            return match.group()
        else:
            return None

    @staticmethod
    def __number_of_pages(link_string):
        match = re.search('(?<=<)[\\S]*page=(\\d+)(?=>; rel="last")', link_string)
        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def __get_token():
        with open("../resources/token.txt", "r") as token_file:
            token = token_file.readline()
            if token != "":
                return token
        raise AssertionError("Token file could not be read")
