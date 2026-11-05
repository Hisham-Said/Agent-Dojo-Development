from config import LLM_PROVIDER

from .gemini_provider import GeminiProvider
from .groq_provider import GroqProvider


def create_provider(provider_name=None):

    provider_name = (
        provider_name or LLM_PROVIDER
    ).lower()

    if provider_name == "gemini":
        return GeminiProvider()

    if provider_name == "groq":
        return GroqProvider()

    raise ValueError(
        f"Unsupported provider: {provider_name}"
    )