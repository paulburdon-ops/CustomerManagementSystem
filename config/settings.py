from dotenv import load_dotenv
import os

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b",
)