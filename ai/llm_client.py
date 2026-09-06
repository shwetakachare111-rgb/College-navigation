"""Reserved integration point: read API keys from environment, never source."""
import os


def api_key_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))
