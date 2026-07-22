from models.customer import Customer


customer = Customer(
    id=1,
    name="Amazon",
    account="AMZ001"
)

print(customer)

print(customer.name)
print(customer.account)
print(customer.id)

customer.name = "Tesco"

print(customer)