import json

from src.util.GithubApiPageIterator import GithubApiPageIterator

iterator = GithubApiPageIterator("https://api.github.com/repos/tensorflow/tensorflow/pulls", params={"page": "1", "per_page": 100})

print(iterator.total_pages)

# count = 0
# for page in iterator:
#     for element in page:
#         count += 1
#         print("pr", count)

