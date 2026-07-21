from flask import Flask, abort, redirect, render_template, request, url_for

import customer_storage

app = Flask(__name__)


@app.route("/")
def dashboard():
    customers = customer_storage.get_all_customers()

    return render_template(
        "dashboard.html",
        customer_count=len(customers),
        current_page="dashboard",
    )


@app.route("/customers")
def list_customers():
    customers = customer_storage.get_all_customers()

    return render_template(
        "customers.html",
        customers=customers,
        current_page="customers",
    )

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["name"]
        account = request.form["account"]

        customer_storage.add_customer(
            name=name,
            account=account,
        )

        return redirect(url_for("list_customers"))

    return render_template(
        "customer_form.html",
        current_page="customers",
    )
@app.route("/customers/<int:customer_id>")
def view_customer(customer_id):
    customer = customer_storage.get_customer(customer_id)

    if customer is None:
        abort(404)

    return render_template(
        "customer_detail.html",
        customer=customer,
        current_page="customers",
    )

if __name__ == "__main__":
    app.run(debug=True)
