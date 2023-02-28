class ProjectListReader:

    def __init__(self, path):
        file = open(path, "r")
        self.projects = file.readlines()

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.projects):
            raise StopIteration
        project_name = self.projects[self.index].split("/")[-1]
        project_url = self.projects[self.index]
        self.index += 1
        return project_name, project_url
