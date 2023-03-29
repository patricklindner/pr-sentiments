import matplotlib.pyplot as plt
from scipy.stats import linregress
import pandas as pd

EXPLANTORY_VARIABLES = [
    "body_polarity",
    "body_subjectivity",
    "author_comment_polarity",
    "author_comment_subjectivity",
    "reviewer_comment_polarity",
    "reviewer_comment_subjectivity"
]
CONTROLLED_VARIABLES = [
    "added_lines",
    "removed_lines",
    "commits",
    "changed_files",
    "is_weekend",
    "project_size",
    "project_age",
    "comment_count",
    "comment_participants",
    "author_pr_count"
]


def explore_distribution(df):
    print_correlation_matrix(df)
    plot_distribution(df, [
        'time_to_merge', 'project_age', 'project_size', 'commits',
        'comment_count', 'comment_participants', 'author_pr_count'
    ])
    plot_distribution(df, EXPLANTORY_VARIABLES)
    plot_scatter_controlled(df)
    plot_scatter_explanatory(df)


def print_correlation_matrix(df):
    df_colleration = df.corr(method='pearson')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(df_colleration)


def plot_distribution(df, cols):
    fig, axes = plt.subplots()
    axes.violinplot(dataset=[df[c].values for c in cols])
    axes.set_title('Distribution of variables')
    axes.yaxis.grid(True)
    axes.set_xlabel('Normalized values')
    plt.ylim(-2.5, 2.5)
    plt.xticks(list(range(1, len(cols) + 1)), cols, rotation=20)
    plt.show()


def plot_scatter_controlled(df):
    for controlled in CONTROLLED_VARIABLES:
        plot_with_best_fit(df, controlled, 'time_to_merge', line_color='b')


def plot_scatter_explanatory(df):
    for explantory in EXPLANTORY_VARIABLES:
        plot_with_best_fit(df, explantory, 'time_to_merge')


def plot_with_best_fit(df, xs: str, ys: str, line_color='r'):
    x_range = (-5 < df[xs]) & (df[xs] < 5)
    y_range = (-5 < df[ys]) & (df[ys] < 5)
    df = df[x_range & y_range]
    plt.scatter(df[xs], df[ys], s=0.15)
    m, c, r, p, std_err = linregress(df[xs], df[ys])
    # plot line: y = m*x + c
    plt.plot(df[xs], c + m*df[xs], line_color, label='best fit line')
    plt.legend(('data', 'best-fit'))
    plt.title((
        f"Linear correlation between {xs} and {ys} found with\nslope:{m:.2}, "
        f"intercept:{c:.2}, r:{r:.2}, p:{p:.2}, str_error:{std_err:.2}"
    ))
    plt.xlabel(xs + " normalized")
    plt.ylabel(ys + " normalized")
    plt.show()
