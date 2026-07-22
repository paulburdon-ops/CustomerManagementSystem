import logging
import sqlite3
from pathlib import Path

from models import Customer


DATABASE_FILE = Path(__file__).parent / "customers.db"


def _create_customer_from_row(row: tuple) -> Customer:
    return Customer(
        id=row[0],
        name=row[1],
        account=row[2],
    )


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
                INSERT INTO customers (
                    name,
                    account
                )
                VALUES (?, ?)
                """,
                (name, account),
            )

        logging.info(
            "Customer added: %s (%s)",
            name,
            account,
        )
        return True

    except sqlite3.IntegrityError:
        logging.warning(
            "Duplicate account attempted: %s",
            account,
        )
        return False

    except sqlite3.Error as error:
        logging.error(
            "Database error while adding %s: %s",
            account,
            error,
        )
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

        return [
            _create_customer_from_row(row)
            for row in rows
        ]


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

        return _create_customer_from_row(row)


def get_customer(customer_id: int) -> Customer | None:
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

        row = cursor.fetchone()

        if row is None:
            return None

        return _create_customer_from_row(row)


def search_customers(search: str) -> list[Customer]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                account
            FROM customers
            WHERE
                account LIKE ?
                OR name LIKE ?
            ORDER BY name
            """,
            (
                f"%{search}%",
                f"%{search}%",
            ),
        )

        rows = cursor.fetchall()

        return [
            _create_customer_from_row(row)
            for row in rows
        ]


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
                    "Attempted to update non-existent account: %s",
                    account,
                )
                return False

        logging.info(
            "Customer updated: %s -> %s",
            account,
            name,
        )
        return True

    except sqlite3.Error as error:
        logging.error(
            "Database error while updating %s: %s",
            account,
            error,
        )
        return False


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
                    "Attempted to delete non-existent account: %s",
                    account,
                )
                return False

        logging.info(
            "Customer deleted: %s",
            account,
        )
        return True
    
    

    except sqlite3.Error as error:
        logging.error(
            "Database error while deleting %s: %s",
            account,
            error,
        )
        return False
    
    
def get_customer_count():
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT COUNT(*)
            FROM customers
            """
        )

        return cursor.fetchone()[0]
    
def get_recent_customers(limit=5):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                account
            FROM customers
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        return [_create_customer_from_row(row) for row in rows]