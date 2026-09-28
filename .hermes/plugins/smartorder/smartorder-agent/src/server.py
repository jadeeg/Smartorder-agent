from pathlib import Path
import json

from flask import Flask, jsonify, request


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "orders.json"


def load_orders():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise RuntimeError(
            f"Orders file not found: {DATA_PATH}"
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Invalid JSON in {DATA_PATH}: {error}"
        )


orders = load_orders()


@app.get("/orders/<order_id>")
def get_order(order_id):
    order = next(
        (
            order for order in orders
            if order["orderId"] == order_id
        ),
        None
    )

    if not order:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order)


@app.get("/orders")
def find_order():
    email = request.args.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    matching_orders = [
        order for order in orders
        if order["email"].lower() == email.lower()
    ]

    return jsonify(matching_orders)


@app.get("/customer/orders/<order_id>")
def get_customer_order(order_id):
    email = request.args.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    order = next(
        (
            order for order in orders
            if order["orderId"] == order_id
            and order["email"].lower() == email.lower()
        ),
        None
    )

    if not order:
        return jsonify({
            "error": "Order not found or verification failed"
        }), 404

    return jsonify({
        "orderId": order["orderId"],
        "product": order["product"],
        "size": order["size"],
        "status": order["status"],
        "shippingDate": order["shippingDate"],
        "estimatedDelivery": order["estimatedDelivery"]
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
