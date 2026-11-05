from environments.workspace import WorkspaceEnvironment


environment = WorkspaceEnvironment()


def search_files(query):
    return environment.search_files(query)


def read_file(file_id):
    return environment.read_file(file_id)