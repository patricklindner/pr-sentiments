from src.util.ProjectListReader import ProjectListReader

reader = ProjectListReader("../resources/project-list.txt")


for name, url in reader:
    print(name, url)
