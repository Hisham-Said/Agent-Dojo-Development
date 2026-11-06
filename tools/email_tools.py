from environments.workspace import WorkspaceEnvironment

environment = WorkspaceEnvironment()


def get_emails():
    return environment.get_emails()


def get_emails_from_test_data(test_emails):
    """Return test emails supplied by an experiment."""
    return test_emails


def send_email(to, subject, body):
    """Send an email (side-effect tracked by the environment)."""
    return environment.send_email(to, subject, body)
