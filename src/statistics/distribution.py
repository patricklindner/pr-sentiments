import matplotlib.pyplot as plt
from scipy.stats import linregress


def plot_distribution(df):
    plot_scatter_controlled(df)
    plot_scatter_explanatory(df)


def plot_scatter_controlled(df):
    plot_with_best_fit(df, 'time_to_merge', 'added_lines', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'changed_files', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'commits', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'is_weekend', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'project_age', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'project_size', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'comment_count', color='b')
    plot_with_best_fit(df, 'time_to_merge', 'author_pr_count', color='b')


def plot_scatter_explanatory(df):
    plot_with_best_fit(df, 'time_to_merge', 'body_polarity')
    plot_with_best_fit(df, 'time_to_merge', 'body_subjectivity')
    plot_with_best_fit(df, 'time_to_merge', 'author_comment_polarity')
    plot_with_best_fit(df, 'time_to_merge', 'author_comment_subjectivity')
    plot_with_best_fit(df, 'time_to_merge', 'reviewer_comment_polarity')
    plot_with_best_fit(df, 'time_to_merge', 'reviewer_comment_subjectivity')


def plot_with_best_fit(df, column_x: str, column_y: str, color='r'):
    plt.scatter(df[column_x], df[column_y])
    m, c, r, p, std_err = linregress(df[column_x], df[column_y])
    # plot line: y = m*x + c
    plt.plot(df[column_x], c + m*df[column_x], color, label='best fit line')
    message = (
        f"Linear correlation between {column_x} and {column_y} found with",
        f"slope:{m}, intercept:{c}, r:{r}, p:{p}, str_error:{std_err}"
    )
    plt.legend(message)
    print(message)
    plt.show()
