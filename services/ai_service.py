from pathlib import Path

from click import prompt

from models.customer import Customer
from ai.openai_client import generate_text as openai_generate
from ai.ollama_client import generate_text as ollama_generate

from config.settings import AI_PROVIDER


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = PROJECT_ROOT / "prompts" / "customer_summary.md"



def generate_summary(customer: Customer) -> str:
    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

    prompt = (
        prompt_template
        .replace("{{name}}", customer.name)
        .replace("{{account}}", customer.account)
    )

    if AI_PROVIDER.lower() == "ollama":
     print("Using Ollama")
     return ollama_generate(prompt)

    print("Using OpenAI")
    return openai_generate(prompt)