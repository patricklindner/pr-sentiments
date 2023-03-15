import os.path
import re

import requests
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode

FAILED_REQUESTS_FILE = "../logs/failed-requests.txt"

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
        self.jumped = False
        self.page_number = 0
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
            if 200 <= resp.status_code <= 300:
                print("Fetched from:", resp.url)
                self.next_url = self.__extract_next_link(resp.headers.get("link"))
                self.page_number += 1
                return resp.json()
            else:
                print("Something went wrong while fetching url", resp.url)
                print("logging failed url to file")
                if os.path.exists(FAILED_REQUESTS_FILE):
                    write_mode = "a"
                else:
                    write_mode = "w"
                with open(FAILED_REQUESTS_FILE, write_mode) as failed_log_file:
                    failed_log_file.write(resp.url + "\n")

    def jump(self, collection_size):
        """
        This function jumps after the first duplicate is found several pages.

        Args:
            collection_size (int): The number of rows in mongoDB table
        """
        if self.jumped:
            return
        self.jumped = True

        parsed = urlparse(self.next_url)
        query_filters = parse_qs(parsed.query)
        query_filters = {key: query_filters[key][0] for key in query_filters}
        per_page = query_filters['per_page']
        self.page_number = collection_size // int(per_page) + 1

        if self.page_number >= self.total_pages:
            self.next_url = None
        else:
            query_filters['page'] = self.page_number
            self.next_url = ParseResult(
                scheme=parsed.scheme,
                netloc=parsed.hostname,
                path=parsed.path,
                params=parsed.params,
                query=urlencode(query_filters),
                fragment=parsed.fragment
            ).geturl()

    def print_progress(self):
        percent = self.page_number / self.total_pages * 100
        print(f"progress {percent:.2f}%")

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
