from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    account: str
    name: str