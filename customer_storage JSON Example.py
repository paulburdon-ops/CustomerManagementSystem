import json
from pathlib import Path


CUSTOMER_FILE = Path(__file__).parent / "customers.json"


def load_customers():
    with open(CUSTOMER_FILE, "r", encoding="utf-8") as file:
        customers = json.load(file)

    return customers


def save_customers(customers):
    with open(CUSTOMER_FILE, "w", encoding="utf-8") as file:
        json.dump(customers, file, indent=4)