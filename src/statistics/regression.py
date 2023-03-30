from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

RESPONSE_VARIABLE = "time_to_merge"
EXPLANTORY_VARIABLES = [
    "body_polarity",
    "body_subjectivity",
    "author_comment_polarity",
    "author_comment_subjectivity",
    "reviewer_comment_polarity",
    "reviewer_comment_subjectivity"
]
CONTROLLED_VARIABLES = [  # Take all variables p < .05 and slope > .01
    "added_lines",  # slope = 0.058, p = 0.019
    "removed_lines",  # slope = 0.049, p = 0.11
    "commits",  # slope = 0.97, p = 0.00
    "changed_files",  # slope = .056, p = .00043
    "is_weekend",  # slope = 0.011, p = .034
    "project_size",  # slope = 0.012, p = 0.014
    # project_age ignored because slope = 0.0082! p = 0.099!
    "comment_count",  # slope = 0.053, p = 0
    "comment_participants",  # slope = 0.035, p = 0
    "author_pr_count",  # slope = -0.033, p = 0
]


def plot_regression(data):
    model, predicted = multilinear_regression(data)
    for coef, var in zip(model.coef_, EXPLANTORY_VARIABLES):
        xs = data[var]
        ys = data[RESPONSE_VARIABLE] - predicted['predicted'] + coef * xs
        plot_me_daddy(xs, ys, coef, model.intercept_)


def multilinear_regression(data):
    model = LinearRegression()
    X = data[EXPLANTORY_VARIABLES + CONTROLLED_VARIABLES]
    y = data[RESPONSE_VARIABLE]
    model.fit(X.values, y.values)
    predicted = model.predict(X.values)

    print(f"R2 = {model.score(X.values, y.values):.3f}")
    for coef, var in zip(model.coef_, X.columns):
        print(f"{var} has a coeffient of {coef:.3f}")

    return model, pd.DataFrame(predicted, columns=['predicted'])


def plot_me_daddy(xs, ys, coef, inter):
    plt.scatter(xs, ys, s=0.15)
    plt.plot(xs, inter + coef*xs, 'r')
    plt.legend(('data', 'best-fit'))
    plt.title(
        f"""Multilinear regression between polarity and time to merge
        Slope = {coef:.2} and intercept = {inter:.2}"""
    )
    plt.xlabel("Polarity normalized")
    plt.ylabel("Time to Merge normalized")
    plt.show()
