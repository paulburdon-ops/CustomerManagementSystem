import sqlite3
import logging
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


def add_customer(name: str, account: str) -> bool:
    try:
        with get_connection() as connection:
            connection.execute(
              """
              INSERT INTO customers (name, account)
              VALUES (?, ?)
              """,
              (name, account),
        )
        logging.info(f"Customer added: {name} ({account})")
        return True

    except sqlite3.IntegrityError:
        logging.warning(f"Duplicate account attempted: {account}")
        return False

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
    


def delete_customer(account: str) -> bool:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM customers
                WHERE account = ?
                """,
                (account,),
            )

            if cursor.rowcount == 0:
                logging.warning(
                    f"Attempted to delete non-existent account: {account}"
                )
                return False

            logging.info(f"Customer deleted: {account}")
            return True

    except sqlite3.Error as error:
        logging.error(f"Database error while deleting {account}: {error}")
        return False


def update_customer(account: str, name: str) -> bool:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE customers
                SET name = ?
                WHERE account = ?
                """,
                (name, account),
            )

            if cursor.rowcount == 0:
                logging.warning(
                    f"Attempted to update non-existent account: {account}"
                )
                return False

            logging.info(f"Customer updated: {account} -> {name}")
            return True

    except sqlite3.Error as error:
        logging.error(f"Database error while updating {account}: {error}")
        return False
    

def get_customer(customer_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                account
            FROM customers
            WHERE id = ?
            """,
            (customer_id,),
        )

        return cursor.fetchone()