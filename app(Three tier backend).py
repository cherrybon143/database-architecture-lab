from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Home route to serve HTML
@app.route("/")
def index():
    return render_template("index.html")

# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products])

# Add a new product
@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    if not data or "name" not in data or "price" not in data or "stock" not in data:
        return jsonify({"error": "Invalid request data"}), 400
    
    new_product = Product(name=data["name"], price=data["price"], stock=data["stock"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": f"Product '{new_product.name}' added successfully!"}), 201

# Delete a product
@app.route("/delete_product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product '{product.name}' deleted successfully!"}), 200
    return jsonify({"error": "Product not found"}), 404

# Initialize the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
