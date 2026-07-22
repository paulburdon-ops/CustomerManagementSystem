import requests

from config.settings import OLLAMA_MODEL


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_text(prompt: str) -> str:
    print("Sending request to Ollama...")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    print("Response received")

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()