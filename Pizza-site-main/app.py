from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
from functools import wraps
from collections import Counter
from forms import SignupForm, LoginForm
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.secret_key = 'a44a55a0470aecd2d9dfc27f701bb8a2'
app.config["MONGO_URI"] = "mongodb+srv://12subratpandey:f08DLSNuuOBCn62J@cluster0.uoeorft.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connected to MongoDB

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# CSRF Error Handler
@app.errorhandler(400)
def handle_csrf_error(e):
    if "CSRF" in str(e):
        flash("CSRF token validation failed. Please try again.", "danger")
        return redirect(request.referrer or url_for('home'))
    return e

# ----- Pizza Items -----
PIZZAS = [
    {"id": 1, "name": "Margherita", "price": 249, "veg": True, "img": "pizza1.jpg"},
    {"id": 2, "name": "Pepperoni", "price": 299, "veg": False, "img": "pizza2.jpg"},
    {"id": 3, "name": "Veggie Supreme", "price": 279, "veg": True, "img": "pizza3.jpg"},
    {"id": 4, "name": "BBQ Chicken", "price": 319, "veg": False, "img": "pizza4.jpg"},
    {"id": 5, "name": "Farmhouse", "price": 269, "veg": True, "img": "pizza5.jpg"},
    {"id": 6, "name": "Cheese Burst", "price": 299, "veg": True, "img": "pizza6.jpg"},
    {"id": 7, "name": "Chicken Tikka", "price": 329, "veg": False, "img": "pizza7.jpg"},
    {"id": 8, "name": "Paneer Makhani", "price": 289, "veg": True, "img": "pizza8.jpg"},
    {"id": 9, "name": "Corn Delight", "price": 259, "veg": True, "img": "pizza9.jpg"},
    {"id": 10, "name": "Meat Lovers", "price": 349, "veg": False, "img": "pizza10.jpg"},
    {"id": 11, "name": "Mexican Veg", "price": 299, "veg": True, "img": "pizza11.jpg"},
    {"id": 12, "name": "Butter Chicken", "price": 349, "veg": False, "img": "pizza12.jpg"},
]

# ----- Decorator -----
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please login to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----- Routes -----

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('menu'))
    form = SignupForm()
    if form.validate_on_submit():
        users = mongo.db.users
        if users.find_one({"email": form.email.data}):
            flash("Email already exists. Please log in.", "warning")
            return redirect(url_for('login'))

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users.insert_one({
            "username": form.username.data,
            "email": form.email.data,
            "gender": form.gender.data,
            "password": hashed_pw
        })
        flash("Account created successfully!", "success")
        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('menu'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            session['user'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('menu'))
        else:
            flash("Invalid credentials.", "danger")
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    return render_template('menu.html', pizzas=PIZZAS, title="Menu")

@app.route('/add_to_cart', methods=["POST"])
@login_required
def add_to_cart():
    pizza_id = int(request.form['pizza_id'])
    cart = session.get("cart", [])
    cart.append(pizza_id)
    session["cart"] = cart
    flash("Pizza added to cart!", "success")
    return redirect(url_for('menu'))

@app.route('/cart')
@login_required
def cart():
    cart_ids = session.get("cart", [])
    cart_counter = Counter(cart_ids)

    cart_items = []
    total = 0
    for pizza_id, qty in cart_counter.items():
        pizza = next((p for p in PIZZAS if p["id"] == pizza_id), None)
        if pizza:
            item = pizza.copy()
            item["quantity"] = qty
            item["subtotal"] = qty * item["price"]
            total += item["subtotal"]
            cart_items.append(item)

    return render_template("cart.html", cart=cart_items, total=total, title="Cart")

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    pizza_id = int(request.form['pizza_id'])
    action = request.form['action']
    cart = session.get("cart", [])

    if action == "add":
        cart.append(pizza_id)
    elif action == "remove" and pizza_id in cart:
        cart.remove(pizza_id)

    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route('/clear_cart')
@login_required
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    payment_method = request.form.get('payment_method')
    session.pop("cart", None)
    flash(f"Order placed successfully using {payment_method}!", "success")
    return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
@login_required
def order_confirmation():
    return render_template('order_confirmation.html', title="Order Confirmation")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
