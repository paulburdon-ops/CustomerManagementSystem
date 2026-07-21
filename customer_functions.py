import customer_storage




def list_customers():
 customers = customer_storage.get_all_customers()

 for customer in customers:
    print(customer)

def find_customer_by_name(name):
    customers = customer_storage.load_customers()

    for customer in customers:
        if customer["name"].lower() == name.lower():
            return customer

    return None

def add_customer(name, account):
    customers = customer_storage.load_customers()

    new_customer = {
        "name": name,
        "account": account
    }

    customers.append(new_customer)

    customer_storage.save_customers(customers)

    return new_customer

