import matplotlib.pyplot as plt

from util.ProjectListReader import ProjectListReader
from util.mongo import get_database


def plot_comments_per_pr(collection_name, file_name=None):
    project_list = ProjectListReader("../resources/project-list.txt")
    db = get_database(collection_name)
    x_axis = []
    y_axis = []
    for _, repo in project_list:
        x_axis.append(repo)
        comments = []
        for pr in db[repo].find():
            comments.append(len(pr["comments"]))
        y_axis.append(sum(comments) / len(comments))

    plt.bar(x_axis, y_axis)
    plt.title('Average Number of Comments per PR per Project')
    # plt.ylabel('Average number of comments per PR')
    # plt.xlabel('Project')
    plt.xticks(rotation=50)
    plt.tight_layout()
    if file_name is not None:
        plt.savefig(f"../figs/{file_name}.png")
    plt.show()


def plot_pull_requests(collection_name, file_name=None):
    project_list = ProjectListReader("../resources/project-list.txt")
    db = get_database(collection_name)
    labels = []
    values = []
    for _, repo in project_list:
        value = db[repo].count_documents({})
        values.append(value)
        labels.append(repo)

    patches, texts = plt.pie(values)
    plt.legend(patches, labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.subplots_adjust(right=0.7)
    if file_name is not None:
        plt.savefig(f"../figs/{file_name}.png")
    plt.show()


plot_pull_requests("pull-requests-raw", "pr_proportion_raw")
plot_pull_requests("pull-requests-clean", "pr_proportion_clean")
plot_pull_requests("pull-requests-sentiment-clean", "pr_proportion_sentiment_clean")


plot_comments_per_pr("pull-requests-enriched", "comments_per_pr_enriched")
plot_comments_per_pr("pull-requests-sentiment-clean", "comments_per_pr_sentiment_clean")
