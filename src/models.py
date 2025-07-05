from bson import ObjectId
from datetime import datetime
from db import mongo

# USER
def create_user(username, email, hashed_password):
    return mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

# PIZZA
def add_pizza(name, base_price):
    return mongo.db.pizzas.insert_one({
        "name": name,
        "base_price": base_price
    })

# VARIANT
def add_variant(pizza_id, size, crust, price):
    return mongo.db.variants.insert_one({
        "pizza_id": ObjectId(pizza_id),
        "size": size,
        "crust": crust,
        "price": price
    })

# ORDER
def place_order(user_id, items, total_price, name, address, phone):
    return mongo.db.orders.insert_one({
        "user_id": ObjectId(user_id),
        "items": items,
        "total_price": total_price,
        "customer_name": name,
        "address": address,
        "phone": phone,
        "timestamp": datetime.utcnow()
    })

# CONTACT
def save_contact(name, email, message):
    return mongo.db.contacts.insert_one({
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.utcnow()
    })

# CART
def save_cart(username, cart_items):
    return mongo.db.carts.update_one(
        {"username": username},
        {"$set": {"cart": cart_items, "timestamp": datetime.utcnow()}},
        upsert=True
    )

def get_cart(username):
    return mongo.db.carts.find_one({"username": username})
