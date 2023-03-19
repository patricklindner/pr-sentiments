import os.path
import re
import logging

import requests
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode

FAILED_REQUESTS_FILE = "../logs/failed-requests.log"


class GithubApiPageIterator:

    def __init__(self, project_name, url, params=None):
        self.start_url = url
        self.initial_params = params
        self.token = self.__get_token()
        self.fetched_result = None
        self.total_pages = 0
        self.project_name = project_name
        self.current_page = 0
        self.log = logging.getLogger(project_name)

    def __iter__(self):
        self.next_url = self.start_url
        self.jumped = False
        self.current_page = 0
        # initial request has to be made here in order to find the total number of pages
        self.log.info("Fetching initial page from: " + self.start_url+"?"+urlencode(self.initial_params))
        resp = requests.get(
            url=self.start_url,
            params=self.initial_params,
            headers={"Authorization": "Bearer " + self.token}
        )
        if resp.headers.get("link") is not None:
            self.total_pages = int(self.__number_of_pages(resp.headers.get("link")))
        else:
            self.total_pages = 1
        self.log.info(f"Number of total pages: {self.total_pages}")
        self.__handle_response(resp)
        return self

    def __len__(self):
        return self.total_pages

    def __next__(self):
        if self.fetched_result is None:
            raise StopIteration

        return_value = self.fetched_result
        if self.next_url is not None:
            self.log.info(f"Fetching page from {self.next_url}")
            resp = requests.get(
                url=self.next_url,
                headers={"Authorization": "Bearer " + self.__get_token()}
            )
            self.__handle_response(resp)
        else:
            self.fetched_result = None
        self.current_page += 1
        return return_value

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
        self.current_page = collection_size // int(per_page) + 1

        if self.current_page >= self.total_pages:
            self.next_url = None
        else:
            query_filters['page'] = self.current_page
            self.next_url = ParseResult(
                scheme=parsed.scheme,
                netloc=parsed.hostname,
                path=parsed.path,
                params=parsed.params,
                query=urlencode(query_filters),
                fragment=parsed.fragment
            ).geturl()

    def __handle_response(self, resp):
        if 200 <= resp.status_code < 300:
            self.fetched_result = resp.json()
            self._set_next_url(resp)
        else:
            self.__handle_http_error(resp)

    def __handle_http_error(self, resp):
        self.log.warning(f"Something went wrong while fetching url {resp.url}")
        self.log.warning("logging failed url to file")
        if os.path.exists(FAILED_REQUESTS_FILE):
            write_mode = "a"
        else:
            write_mode = "w"
        with open(FAILED_REQUESTS_FILE, write_mode) as failed_log_file:
            failed_log_file.write(resp.url + "\n")

    def _set_next_url(self, resp):
        if resp.headers.get("link") is not None:
            self.next_url = self.__extract_next_link(resp.headers.get("link"))
        else:
            self.next_url = None

    @staticmethod
    def __extract_next_link(link_string):
        match = re.search('(?<=<)([\\S]*)(?=>; rel="next")', link_string)
        if match:
            return match.group()
        else:
            return None

    def __number_of_pages(self, link_string):
        self.log.info(f"link string {link_string}")
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
