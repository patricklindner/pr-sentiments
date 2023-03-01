import re

import requests


class GithubApiPageIterator:

    def __init__(self, url, params={}):
        self.start_url = url
        self.params = params

    def __iter__(self):
        self.next_url = self.start_url
        return self

    def __next__(self):
        if self.next_url is None:
            raise StopIteration
        else:
            print("Fetching from url", self.next_url)
            resp = requests.get(self.next_url, params=self.params)
            link = resp.headers.get("link")
            match = re.search('(?<=<)([\\S]*)(?=>; rel="next")', link)
            if match:
                self.next_url = match.group()
            else:
                self.next_url = None

            return resp.json()
