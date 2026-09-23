 
 
from flask import Flask, jsonify, request 
import json

app = Flask(__name__)

with open("data/orders.json", "r") as file:
    orders = json.load(file)
    
    
@app.get("/orders/<order_id>")
def get_order(order_id):
    order = next(
        (order for order in orders if order["orderId"] == order_id),
        None
    )
    
    if not order:
        return jsonify({"error": "Order not found" }), 404
    
    return jsonify(order)

@app.get("/orders")
def find_order():
    email = request.args.get("email")
    
    matching_orders =[
        order for order in orders
        if order["email"].lower() == email.lower()
        
    ]
    return jsonify(matching_orders)

if __name__ == "__main__":
    app.run(port=5000, debug =True)
    
    
    
