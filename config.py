import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3-flash-preview"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

MAX_AGENT_STEPS = int(
    os.getenv("MAX_AGENT_STEPS", "10")
)

if LLM_PROVIDER not in {"gemini", "groq"}:
    raise ValueError(
        "LLM_PROVIDER must be either 'gemini' or 'groq'"
    )