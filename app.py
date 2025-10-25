from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from flask import send_from_directory
import random

app = Flask(__name__)
app.secret_key = "secret123"

# --- Product Data ---
products = {
    "vegetables": [
        {"id": 1, "name": "Tomato", "price": 40, "image": "tomato.jpg"},
        {"id": 2, "name": "Onion Small", "price": 30, "image": "onion_small.jpg"},
        {"id": 3, "name": "Onion Big", "price": 50, "image": "onion_big.jpg"},
        {"id": 4, "name": "Mushroom Button", "price": 120, "image": "mushroom.jpg"},
        {"id": 5, "name": "Potato Baby", "price": 35, "image": "potato_baby.jpg"},
        {"id": 6, "name": "Potato Normal", "price": 30, "image": "potato_normal.jpg"},
        {"id": 7, "name": "Beans", "price": 60, "image": "beans.jpg"},
        {"id": 8, "name": "Pumpkin", "price": 25, "image": "pumpkin.jpg"},
        {"id": 9, "name": "Cauliflower", "price": 50, "image": "cauliflower.jpg"},
        {"id": 10, "name": "Cucumber", "price": 20, "image": "cucumber.jpg"},
        {"id": 11, "name": "Drumstick", "price": 70, "image": "drumstick.jpg"},
        {"id": 12, "name": "Bottle Gourd", "price": 30, "image": "bottle_gourd.jpg"},
        {"id": 13, "name": "Lady Finger", "price": 40, "image": "lady_finger.jpg"},
        {"id": 14, "name": "Snake Gourd", "price": 35, "image": "snake_gourd.jpg"},
        {"id": 15, "name": "Raw Banana", "price": 25, "image": "raw_banana.jpg"},
        {"id": 16, "name": "Carrot", "price": 50, "image": "carrot.jpg"},
        {"id": 17, "name": "Ridge Gourd", "price": 35, "image": "ridge_gourd.jpg"},
        {"id": 18, "name": "Brinjal", "price": 40, "image": "brinjal.jpg"},
        {"id": 19, "name": "Ash Gourd", "price": 30, "image": "ash_gourd.jpg"},
        {"id": 20, "name": "Zucchini Green", "price": 80, "image": "zucchini.jpg"},
        {"id": 21, "name": "Sweet Potato", "price": 60, "image": "sweet_potato.jpg"}
    ],
    "fruits": [
        {"id": 22, "name": "Orange", "price": 60, "image": "orange.jpg"},
        {"id": 23, "name": "Apple", "price": 120, "image": "apple.jpg"},
        {"id": 24, "name": "Coconut", "price": 50, "image": "coconut.jpg"},
        {"id": 25, "name": "Guava", "price": 40, "image": "guava.jpg"},
        {"id": 26, "name": "Banana Red", "price": 35, "image": "banana_red.jpg"},
        {"id": 27, "name": "Tender Coconut", "price": 70, "image": "tender_coconut.jpg"},
        {"id": 28, "name": "Gooseberry", "price": 90, "image": "gooseberry.jpg"},
        {"id": 29, "name": "Watermelon", "price": 50, "image": "watermelon.jpg"},
        {"id": 30, "name": "Grapes", "price": 120, "image": "grapes.jpg"},
        {"id": 31, "name": "Sapota", "price": 40, "image": "sapota.jpg"},
        {"id": 32, "name": "Pineapple", "price": 80, "image": "pineapple.jpg"},
        {"id": 33, "name": "Pomegranate", "price": 100, "image": "pomegranate.jpg"}
    ],
    "leafy_vegetables": [
        {"id": 34, "name": "Coriander Leaves", "price": 20, "image": "coriander.jpg"},
        {"id": 35, "name": "Curry Leaves", "price": 25, "image": "curry_leaves.jpg"},
        {"id": 36, "name": "Mint Leaves", "price": 30, "image": "mint_leaves.jpg"},
        {"id": 37, "name": "Green Chilli", "price": 40, "image": "green_chilli.jpg"},
        {"id": 38, "name": "Garlic", "price": 120, "image": "garlic.jpg"},
        {"id": 39, "name": "Ginger", "price": 80, "image": "ginger.jpg"},
        {"id": 40, "name": "Lemon", "price": 15, "image": "lemon.jpg"},
        {"id": 41, "name": "Arai Keerai (Amaranthus Leaves)", "price": 30, "image": "arai_keerai.jpg"},
        {"id": 42, "name": "Sirukeerai", "price": 25, "image": "sirukeerai.jpg"},
        {"id": 43, "name": "Bajji Milagai (Pikador Green Chilli)", "price": 50, "image": "pikador_green_chilli.jpg"}
    ],
    "spices": [
        {"id": 44, "name": "Chilli Powder", "price": 100, "image": "chilli_powder.jpg"},
        {"id": 45, "name": "Cumin Powder", "price": 80, "image": "cumin_powder.jpg"},
        {"id": 46, "name": "Jeera", "price": 90, "image": "jeera.jpg"},
        {"id": 47, "name": "Garam Masala", "price": 120, "image": "garam_masala.jpg"},
        {"id": 48, "name": "Cardamom", "price": 200, "image": "cardamom.jpg"},
        {"id": 49, "name": "Clove", "price": 250, "image": "clove.jpg"},
        {"id": 50, "name": "Pepper", "price": 150, "image": "pepper.jpg"},
        {"id": 51, "name": "Cinnamon", "price": 180, "image": "cinnamon.jpg"}
    ],
    "snacks": [
        {"id": 52, "name": "Lay's American Cream & Onion", "price": 20, "image": "lays_cream_onion.jpg"},
        {"id": 53, "name": "Kurkure Masala Munch", "price": 20, "image": "kurkure_masala.jpg"},
        {"id": 54, "name": "Lay's West Indies Hot & Sweet Chilli", "price": 25, "image": "lays_hot_sweet_chilli.jpg"},
        {"id": 55, "name": "Parle Hide & Seek Chocolate Biscuits", "price": 30, "image": "parle_hide_seek.jpg"}
    ],
    "drinks": [
        {"id": 56, "name": "Coca Cola", "price": 40, "image": "coca_cola.jpg"},
        {"id": 57, "name": "Pepsi", "price": 40, "image": "pepsi.jpg"},
        {"id": 58, "name": "Fanta", "price": 35, "image": "fanta.jpg"},
        {"id": 59, "name": "Sprite", "price": 35, "image": "sprite.jpg"}
    ]
}



# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        phone = request.form.get("phone")
        # Save the phone in session for later use
        session["phone"] = phone
        # Redirect to main catalog or homepage after login
        return redirect(url_for("catalog"))  # or 'home' if you keep homepage
    return render_template("home.html")

@app.route("/verify_login", methods=["POST"])
def verify_login():
    phone = request.form.get("phone")
    session["phone"] = phone  # store phone number in session
    return redirect(url_for("catalog"))

@app.route("/catalog")
def catalog():
    query = request.args.get("query", "").lower()
    cart_count = sum(session.get("cart", {}).values())  # ✅ Add this line
    return render_template("catalog.html", products=products, query=query, cart_count=cart_count)


@app.route("/category/<category>")
def category_page(category):
    query = request.args.get("query", "").lower()
    items = products.get(category, [])
    if query:
        items = [item for item in items if query in item['name'].lower()]
    cart_count = sum(session.get("cart", {}).values())  # ✅ Add this line
    return render_template("category.html", items=items, query=query, category=category, cart_count=cart_count)


@app.route("/search")
def search_item():
    query = request.args.get("query", "").lower()
    for category, items in products.items():
        for item in items:
            if query in item['name'].lower():
                # Redirect to the category page where the item is found
                return redirect(url_for("category_page", category=category, query=query))
    # If not found, stay on catalog with a message
    return render_template("catalog.html", message=f"No items found for '{query}'")



# --- Add to Cart ---
@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    print(f"✅ Received add_to_cart for item_id={item_id}")  # 👈 keep this line
    data = request.get_json()
    quantity = int(data.get("quantity", 1))

    if "cart" not in session:
        session["cart"] = {}

    item_key = str(item_id)
    if item_key in session["cart"]:
        session["cart"][item_key] += quantity
    else:
        session["cart"][item_key] = quantity

    session.modified = True

    item_name = next((i["name"] for cat in products.values() for i in cat if i["id"] == item_id), "Item")
    return jsonify({"success": True, "name": item_name})




# --- View Cart ---
@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    cart_items = []

    for item_id, qty in cart_data.items():
        for cat_items in products.values():
            for prod in cat_items:
                if prod["id"] == int(item_id):
                    cart_items.append({**prod, "quantity": qty})

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)
    empty = len(cart_items) == 0
    cart_count = sum(session.get("cart", {}).values())
    return render_template("cart.html", cart_items=cart_items, total_price=total_price, empty=empty, cart_count=cart_count)

@app.route("/cart_count")
def cart_count():
    count = sum(session.get("cart", {}).values())
    return jsonify({"count": count})


# --- Update Cart Quantity ---
@app.route("/update_cart/<int:item_id>", methods=["POST"])
def update_cart(item_id):
    data = request.get_json()
    quantity = int(data.get("quantity", 1))

    if "cart" in session and str(item_id) in session["cart"]:
        if quantity > 0:
            session["cart"][str(item_id)] = quantity
        else:
            session["cart"].pop(str(item_id))
        session.modified = True

    return jsonify({"success": True})


# --- Clear Cart ---
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))

# --- Payment Page ---
@app.route("/payment")
def payment():
    cart_data = session.get("cart", {})
    cart_items = []
    for item_id, qty in cart_data.items():
        for cat_items in products.values():
            for prod in cat_items:
                if prod["id"] == int(item_id):
                    cart_items.append({**prod, "quantity": qty})

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)
    cart_count = sum(session.get("cart", {}).values())  # ✅ properly indented
    return render_template(
        "payment.html",
        cart_items=cart_items,
        total_price=total_price,
        cart_count=cart_count
    )  # ✅ same level indentation as the previous line


# --- Complete Payment ---
@app.route("/complete_payment", methods=["POST"])
def complete_payment():
    cart_data = session.get("cart", {})
    cart_items = []

    # Convert cart dict to full item list
    for item_id, qty in cart_data.items():
        for cat_items in products.values():
            for prod in cat_items:
                if prod["id"] == int(item_id):
                    cart_items.append({**prod, "quantity": qty})

    if not cart_items:
        return redirect(url_for("home"))

    payment_method = request.form.get("payment_method", "Not Specified")

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)
    order_id = "NM" + str(random.randint(10000, 99999))
    order_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # Store last order in session
    session["last_order"] = {
        "id": order_id,
        "time": order_time,
        "items": cart_items,
        "total": total_price,
        "payment_method": payment_method
    }

    session.pop("cart", None)  # clear cart after payment
    return redirect(url_for("confirmation"))

# --- Confirmation Page ---
@app.route("/confirmation")
def confirmation():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("home"))  # redirect if no order exists
    return render_template("confirmation.html", order=order)

@app.route('/contact')
def contact():
    cart_count = sum(session.get("cart", {}).values())  # ✅ Add this line
    return render_template('contact.html', cart_count=cart_count)

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')


if __name__ == "__main__":
    app.run(debug=True)
