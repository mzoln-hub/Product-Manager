from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///products.db"
db=SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Float)

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    category = request.form["category"].strip()
    price=request.form["price"].strip()

    if not name:
        flash("Product name cannot be empty")
        return redirect("/")

    if not category:
        flash("Category cannot be empty")
        return redirect("/")

    try:
        price = float(price)

        if price <= 0:
            flash("Price must be greater than 0")
            return redirect("/")

    except ValueError:
        flash("Price must be a number")
        return redirect("/")

    product = Product(
        name=name,
        category=category,
        price=price
    )

    db.session.add(product)
    db.session.commit()

    return redirect("/")

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_products(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    products = Product.query.filter(
        (Product.name.ilike(f"%{query}%")) |
        (Product.category.ilike(f"%{query}%"))
    ).all()

    return render_template("index.html", products=products)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)