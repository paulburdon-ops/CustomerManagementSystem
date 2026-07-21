import sqlite3
from pathlib import Path

from models import Customer


DATABASE_FILE = Path(__file__).parent / "customers.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_FILE)


def create_customer_table() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account TEXT NOT NULL UNIQUE
            )
            """
        )


def add_customer(name: str, account: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO customers (name, account)
            VALUES (?, ?)
            """,
            (name, account),
        )


def get_all_customers() -> list[Customer]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                account
            FROM customers
            ORDER BY name
            """
        )

        rows = cursor.fetchall()
        customers = []

        for row in rows:
            customer = Customer(
                id=row[0],
                name=row[1],
                account=row[2],
            )
            customers.append(customer)

        return customers


def find_customer(account: str) -> Customer | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                account
            FROM customers
            WHERE account = ?
            """,
            (account,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Customer(
            id=row[0],
            name=row[1],
            account=row[2],
        )


if __name__ == "__main__":
    customers = get_all_customers()

    for customer in customers:
        print(customer)