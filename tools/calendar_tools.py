from environments.workspace import WorkspaceEnvironment


environment = WorkspaceEnvironment()


def get_calendar_events():
    return environment.get_calendar_events()