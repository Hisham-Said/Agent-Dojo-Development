# agent/providers/base_provider.py

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate(self, messages, tools=None):
        """
        Send messages to the LLM.

        Returns:
            LLMResponse
        """
        pass