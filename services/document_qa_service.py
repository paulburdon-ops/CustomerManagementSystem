import json
from pathlib import Path

from ai.ollama_client import generate_text as ollama_generate
from ai.openai_client import generate_text as openai_generate


KNOWLEDGE_FOLDER = Path(__file__).parent.parent / "knowledge"


def load_customer_document(customer_name: str) -> str:
    document_file = KNOWLEDGE_FOLDER / f"{customer_name.lower()}_test.txt"

    if not document_file.exists():
        return "No customer documentation available."

    return document_file.read_text(encoding="utf-8")


def generate_with_provider(
    prompt: str,
    provider: str,
) -> str:
    if provider.lower() == "openai":
        return openai_generate(prompt)

    return ollama_generate(prompt)


def answer_morrisons_question(
    question: str,
    provider: str = "ollama",
) -> dict:
    document_text = load_customer_document("morrisons")

    prompt = f"""
You are BusinessAI, an AI Knowledge Assistant.

You have TWO sources of information:

1. The supplied customer documentation.
2. Your own general knowledge.

Always use the customer documentation first.

If the documentation contains the answer, base your response on it.

If the documentation only partially answers the question, supplement it
with your own general knowledge.

If the documentation does not contain the answer, answer using your own
knowledge and clearly state that the information is not contained in the
customer documentation.

Never invent or guess customer-specific information.

DOCUMENT
========
{document_text}

QUESTION
========
{question}

Respond ONLY with valid JSON.

Use this exact structure:

{{
    "answer": "...",
    "document_information": "...",
    "general_knowledge": "...",
    "confidence": "High",
    "confidence_reason": "...",
    "business_impact": "...",
    "follow_up": [
        "...",
        "..."
    ]
}}

Rules:

- Do not include markdown.
- Do not include code fences.
- Do not include any explanation outside the JSON.
- Always return valid JSON.
- Confidence must be High, Medium or Low.
- Summarise only information directly relevant to the question.
- Do not repeat unrelated information from the document.
"""

    response = generate_with_provider(
        prompt=prompt,
        provider=provider,
    )

    try:
        result = json.loads(response)

    except json.JSONDecodeError:
        result = {
            "answer": response,
            "document_information": "",
            "general_knowledge": "",
            "confidence": "Unknown",
            "confidence_reason": (
                "The AI provider did not return valid JSON."
            ),
            "business_impact": "",
            "follow_up": [],
        }

    result["provider"] = provider.lower()

    return result