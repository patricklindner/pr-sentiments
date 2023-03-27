import matplotlib.pyplot as plt
from scipy.stats import linregress
import pandas as pd


def explore_distribution(df):
    print_correlation_matrix(df)
    plot_scatter_controlled(df)
    plot_scatter_explanatory(df)


def print_correlation_matrix(df):
    df_colleration = df.corr(method='pearson')
    with pd.option_context('display.max_columns', None):
        print(df_colleration)


def plot_scatter_controlled(df):
    plot_with_best_fit(df, 'added_lines', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'changed_files', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'commits', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'is_weekend', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'project_age', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'project_size', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'comment_count', 'time_to_merge', line_color='b')
    plot_with_best_fit(df, 'author_pr_count', 'time_to_merge', line_color='b')


def plot_scatter_explanatory(df):
    plot_with_best_fit(df, 'body_polarity', 'time_to_merge')
    plot_with_best_fit(df, 'body_subjectivity', 'time_to_merge')
    plot_with_best_fit(df, 'author_comment_polarity', 'time_to_merge')
    plot_with_best_fit(df, 'author_comment_subjectivity', 'time_to_merge')
    plot_with_best_fit(df, 'reviewer_comment_polarity', 'time_to_merge')
    plot_with_best_fit(df, 'reviewer_comment_subjectivity', 'time_to_merge')


def plot_with_best_fit(df, xs: str, ys: str, line_color='r'):
    x_range = (-5 < df[xs]) & (df[xs] < 5)
    y_range = (-5 < df[ys]) & (df[ys] < 5)
    df = df[x_range & y_range]
    plt.scatter(df[xs], df[ys])
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
