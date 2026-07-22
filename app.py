from flask import Flask, abort, flash, redirect, render_template, request, url_for
from services.ai_service import generate_summary



import customer_storage

app = Flask(__name__)
app.secret_key = "customerai-development-key"


@app.route("/customers")
def list_customers():

    search = request.args.get("search", "").strip()

    if search:
        customers = customer_storage.search_customers(search)
    else:
        customers = customer_storage.get_all_customers()

    return render_template(
        "customers.html",
        customers=customers,
        search=search,
        current_page="customers",
    )

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["name"]
        account = request.form["account"]

        if customer_storage.add_customer(
            name=name,
            account=account,
        ):
            flash(
                "Customer added successfully.",
        "success"
        )
        else:
            flash(
                "Failed to add customer. Account may already exist.",
                "warning",
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

    ai_summary = generate_summary(customer)

    return render_template(
        "customer_detail.html",
        customer=customer,
        ai_summary=ai_summary,
        current_page="customers",
    )
@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    customer = customer_storage.get_customer(customer_id)

    if customer is None:
        abort(404)

    if request.method == "POST":
        name = request.form["name"]

        if customer_storage.update_customer(
            account=customer.account,
            name=name,
        ):
            flash("Customer updated successfully.", "success")
        else:
            flash("Failed to update customer.", "warning")

        return redirect(url_for("list_customers"))

    return render_template(
        "customer_form.html",
        customer=customer,
        mode="edit",
        current_page="customers",
    )

@app.route("/customers/<int:customer_id>/delete", methods=["GET", "POST"])
def delete_customer(customer_id):

    customer = customer_storage.get_customer(customer_id)

    if customer is None:
        abort(404)

    if request.method == "POST":

        if customer_storage.delete_customer(customer.account):
            flash("Customer deleted successfully.", "success")
        else:
            flash("Failed to delete customer.", "warning")

        return redirect(url_for("list_customers"))

    return render_template(
    "customer_delete.html",
    customer=customer,
    current_page="customers",
)

@app.route("/")
def dashboard():

    customer_count = customer_storage.get_customer_count()

    recent_customers = customer_storage.get_recent_customers()

    return render_template(
        "dashboard.html",
        customer_count=customer_count,
        recent_customers=recent_customers,
        current_page="dashboard",
    )


if __name__ == "__main__":
    app.run(debug=True)

