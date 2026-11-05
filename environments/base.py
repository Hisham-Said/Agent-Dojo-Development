from abc import ABC, abstractmethod


class BaseEnvironment(ABC):

    @abstractmethod
    def get_emails(self):
        pass

    @abstractmethod
    def get_calendar_events(self):
        pass

    @abstractmethod
    def search_files(self, query):
        pass

    @abstractmethod
    def read_file(self, file_id):
        pass

    @abstractmethod
    def snapshot(self):
        """Return a deep copy of the full environment state."""
        pass
