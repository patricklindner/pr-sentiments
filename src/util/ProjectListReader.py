class ProjectListReader:

    def __init__(self, path):
        file = open(path, "r")
        self.projects = file.read().splitlines()

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.projects):
            raise StopIteration
        project = self.projects[self.index].split("/")
        project_name = project[0]
        project_owner = project[1]
        self.index += 1
        return project_owner, project_name
