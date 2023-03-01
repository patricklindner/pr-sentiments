from GithubApiPageIterator import GithubApiPageIterator

iterator = GithubApiPageIterator("https://api.github.com/repos/tensorflow/tensorflow/pulls")
iter(iterator)
print(next(iterator))

