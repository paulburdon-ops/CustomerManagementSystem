from pathlib import Path

from models.customer import Customer
from ai.openai_client import generate_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = PROJECT_ROOT / "prompts" / "customer_summary.md"


def generate_summary(customer: Customer) -> str:
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

    prompt = (
        prompt_template
        .replace("{{name}}", customer.name)
        .replace("{{account}}", customer.account)
    )

    return generate_text(prompt)