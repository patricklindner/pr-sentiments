from src.util.mongo import get_database
from src.util.ProjectListReader import ProjectListReader

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser


DB_NAME = 'pull-requests-raw'
BAR_LENGTH = 50
REPO_FILE_PATH = "../resources/project-list.txt"
RESOLUTION = 100


def fn(x, a, b, c):
    return a + b*x[0] + c*x[1]


def main():
    database = get_database(DB_NAME)
    x, y = load_data(database)
    linear_regression(x, y)


def linear_regression(X, Y):
    regressor = LinearRegression()
    regressor.fit(X, Y)

    pred_axis = [i / RESOLUTION for i in range(0, RESOLUTION)]
    avg_0, avg_1 = np.average(X[:, 0]), np.average(X[:, 1])
    Y_pred_0 = regressor.predict([[i, avg_1] for i in pred_axis])
    Y_pred_1 = regressor.predict([[avg_0, i] for i in pred_axis])
    plt.plot(pred_axis, Y_pred_0, color='red')
    plt.plot(pred_axis, Y_pred_1, color='blue')

    plt.scatter(X[:, 0], Y, color='red')
    plt.scatter(X[:, 1], Y, color='blue')
    plt.show()


def load_data(database):
    repo_reader = ProjectListReader(REPO_FILE_PATH)
    x, y = np.empty((0, 2)), np.array([])

    for _, repository in repo_reader:
        repository_collection = database[repository]
        for row in repository_collection.find({}):
            if row['merged_at'] is None:
                continue

            polarity = row['sentiment']['polarity'] / 2 + 0.5
            subjectivity = row['sentiment']['subjectivity']
            new_row = np.array([polarity, subjectivity])
            x = np.vstack([x, new_row])

            merge_time = parser.parse(row['merged_at'])
            created_time = parser.parse(row['created_at'])
            time_to_merge = (merge_time - created_time).total_seconds()
            y = np.append(y, time_to_merge)

    return x, y


if __name__ == "__main__":
    main()
