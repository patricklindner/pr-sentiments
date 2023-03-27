from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader
from src.helpers.loading_bar import print_loading_bar, print_finished_load_bar

from dateutil import parser
import pandas as pd
from pymongo.collection import Collection

from src.statistics.distribution import plot_distribution
from src.statistics.regression import plot_logistic_regression

DB_NAME = 'pull-requests-sentiment-clean'
REPO_FILE_PATH = "./resources/project-list.txt"
DF_COLUMNS = [
    "body_polarity",
    "body_subjectivity",
    "time_to_merge",
    "added_lines",
    "removed_lines",
    "commits",
    "changed_files",
    "is_weekend",
    "project_size",
    "project_age",
    "comment_count",
    "comment_participants",
    "author_pr_count",
    "author_comment_polarity",
    "author_comment_subjectivity",
    "reviewer_comment_polarity",
    "reviewer_comment_subjectivity"
]


def main(in_file: str = None, out_file: str = None):
    if in_file:
        df = pd.read_csv(in_file)
    else:
        database = get_database(DB_NAME)
        df = load_data(database)

    if out_file:
        df.to_csv(out_file)

    normalize_df = (df-df.mean())/df.std()
    # normalize_df.corr('pearson')
    plot_distribution(normalize_df)
    plot_logistic_regression(normalize_df)


def load_data(database) -> pd.DataFrame:
    repo_reader = ProjectListReader(REPO_FILE_PATH)
    df = pd.DataFrame(columns=DF_COLUMNS)
    length = 0

    for _, repository in repo_reader:
        repository_collection = database[repository]
        collection_size = repository_collection.count_documents({})
        print(f'Loading {collection_size} rows from {repository}:')
        load_collection(repository_collection, df, length)
        length += collection_size

    print(f'finished loading {length} rows!')
    return df


def load_collection(collection: Collection, df: pd.DataFrame, shift: int):
    total = collection.count_documents({})
    i = 0
    for row in collection.find():
        df.loc[shift + i] = load_row_data(row)
        i += 1
        print_loading_bar(i, total)
    print_finished_load_bar()


def load_row_data(row: dict) -> list:
    create_time = parser.parse(row['created_at'])
    merge_time = parser.parse(row['merged_at'])
    birth_day = parser.parse(row['project']['created_at'])
    return [
        float(row['body']['polarity']),
        float(row['body']['subjectivity']),
        float((merge_time - create_time).seconds / 60),
        int(row['pull_request']['added']),
        int(row['pull_request']['removed']),
        int(row['pull_request']['commits']),
        int(row['pull_request']['changed_files']),
        bool(create_time.weekday() > 5),
        int(row['project']['size']),
        float((create_time - birth_day).days),
        int(row['comments_count']),
        int(row['comments_participants']),
        int(row['user']['previous_pr_count']),
        float(row['author_comment_average']['polarity']),
        float(row['author_comment_average']['subjectivity']),
        float(row['review_comment_average']['polarity']),
        float(row['review_comment_average']['subjectivity'])
    ]


if __name__ == "__main__":
    print("Lets do some statistical analysis!")
    main(in_file='cache.csv', out_file='cache.csv')
