from config.settings import AI_PROVIDER

from ai.openai_client import generate_text as openai_generate
# from ai.ollama_client import generate_text as ollama_generate


def generate_text(prompt: str) -> str:
    """
    Routes AI requests to the configured provider.
    """

    if AI_PROVIDER == "openai":
        return openai_generate(prompt)

    # if AI_PROVIDER == "ollama":
    #     return ollama_generate(prompt)

    raise ValueError(f"Unknown AI provider: {AI_PROVIDER}")