import json
from copy import deepcopy
from pathlib import Path

from .base import BaseEnvironment


class WorkspaceEnvironment(BaseEnvironment):

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

        # Load initial state into memory so mutations
        # (e.g. injected content) are observable.
        self._emails = self._load_json("emails.json")
        self._calendar = self._load_json("calendar.json")
        self._files = self._load_json("files.json")

        # Track side-effects the agent causes.
        self._sent_emails = []

    def _load_json(self, filename):
        path = self.data_dir / filename

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # Read-only tools
    # ---------------------------------------------------------

    def get_emails(self):
        return self._emails

    def get_calendar_events(self):
        return self._calendar

    def search_files(self, query):
        query = query.lower()

        return [
            file
            for file in self._files
            if query in file.get("name", "").lower()
            or query in file.get("content", "").lower()
        ]

    def read_file(self, file_id):
        for file in self._files:
            if file.get("id") == file_id:
                return file

        return {
            "error": f"File with id {file_id} not found."
        }

    # ---------------------------------------------------------
    # Write tools (side-effects)
    # ---------------------------------------------------------

    def send_email(self, to, subject, body):
        email = {
            "to": to,
            "subject": subject,
            "body": body,
        }
        self._sent_emails.append(email)
        return {"status": "sent", "email": email}

    # ---------------------------------------------------------
    # State management
    # ---------------------------------------------------------

    def snapshot(self):
        """Return a deep copy of the full environment state."""
        return {
            "emails": deepcopy(self._emails),
            "calendar": deepcopy(self._calendar),
            "files": deepcopy(self._files),
            "sent_emails": deepcopy(self._sent_emails),
        }

    @classmethod
    def from_snapshot(cls, state, data_dir="data"):
        """Create an environment from a previously captured snapshot."""
        env = cls.__new__(cls)
        env.data_dir = Path(data_dir)
        env._emails = deepcopy(state["emails"])
        env._calendar = deepcopy(state["calendar"])
        env._files = deepcopy(state["files"])
        env._sent_emails = deepcopy(state.get("sent_emails", []))
        return env
