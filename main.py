import customer_functions
import customer_storage


customer_storage.create_customer_table()

print("Customer database is ready.")

running = True

while running:
    print()
    print("Choose an option:")
    print("1. List all customers")
    print("2. Find customer by account")
    print("3. Add new customer JSON")
    print("4. Add new customer SQLite")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        customers = customer_storage.get_all_customers()

        for customer in customers:
            print(customer.name)

    elif choice == "2":
        account = input("Enter account number: ")

        customer = customer_storage.find_customer(account)

        if customer is None:
            print("Customer not found.")
        else:
            print(f"Name: {customer.name}")
            print(f"Account: {customer.account}")

    elif choice == "3":
        name = input("Enter customer name: ")
        account = input("Enter account number: ")

        customer = customer_functions.find_customer_by_name(name)

        if customer:
            print(
                f"Customer found: {customer['name']} "
                f"with account {customer['account']}"
            )
        else:
            customer = customer_functions.add_customer(name, account)

            print(
                f"Customer added: {customer['name']} "
                f"with account {customer['account']}"
            )

    elif choice == "4":
         name = input("Enter customer name: ")
         account = input("Enter account number: ")

         customer_added = customer_storage.add_customer(name, account)

         if customer_added:
          print("Customer added successfully.")
         else:
          print(f"A customer with account {account} already exists.")

    elif choice == "5":
        running = False

    else:
        print("Invalid option.")

print("Exiting the program.")