import customer_functions
import customer_storage
import logging
import logger_config

def list_customers():
    customers = customer_storage.get_all_customers()

    print()
    print(f"{'ID':<5}{'Name':<25}{'Account':<15}")
    print("-" * 45)

    for customer in customers:
        print(
            f"{customer.id:<5}"
            f"{customer.name:<25}"
            f"{customer.account:<15}"
        )

def find_customer_by_account():
    account = input("Enter account number: ")
    customer = customer_storage.find_customer(account)

    if customer is None:
        print(f"No customer found with account {account}.")
    else:
        print(f"Customer found: {customer.name} (Account: {customer.account})")

def add_new_customer():
    name = input("Enter customer name: ")
    account = input("Enter account number: ")

    if customer_storage.add_customer(name, account):
        print(f"Customer {name} added successfully.")
    else:
        print(f"Failed to add customer. Account {account} may already exist.")

def delete_customer():
    account = input("Enter account number to delete: ")

    customer = customer_storage.find_customer(account)

    if customer is None:
        print(f"No customer found with account {account}.")
        return

    print()
    print(f"ID      : {customer.id}")
    print(f"Name    : {customer.name}")
    print(f"Account : {customer.account}")
    print()

    confirmation = input("Are you sure you want to delete this customer? (Y/N): ")

    if confirmation.upper() != "Y":
        print("Deletion cancelled.")
        return

    customer_deleted = customer_storage.delete_customer(account)

    if customer_deleted:
        print("Customer deleted successfully.")
    else:
        print("Customer could not be deleted.")

def update_customer():
    account = input("Enter account number to update: ")

    customer = customer_storage.find_customer(account)

    if customer is None:
        print(f"No customer found with account {account}.")
        return

    print()
    print(f"ID      : {customer.id}")
    print(f"Name    : {customer.name}")
    print(f"Account : {customer.account}")
    print()

    new_name = input("Enter new name for the customer: ")

    if not new_name.strip():
        print("Name cannot be empty. Update cancelled.")
        return

    customer_updated = customer_storage.update_customer(account, new_name)

    if customer_updated:
        print("Customer updated successfully.")
    else:
        print("Customer could not be updated.")

customer_storage.create_customer_table()

print("Customer database is ready.")

running = True

while running:
    print()
    print("Choose an option:")
    print("1. List all customers")
    print("2. Find customer by account")
    print("3. Add new customer SQLite")
    print("4. Add Delete customer SQLite")
    print("5. Update customer")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        list_customers()

    elif choice == "2":
        find_customer_by_account()

    
    elif choice == "3":
        add_new_customer()

    elif choice == "3":
        add_new_customer()

    elif choice == "4":
        delete_customer()

    elif choice == "5":
        update_customer()

    elif choice == "6":
        running = False

    else:
        print("Invalid option.")

print("Exiting the program.")