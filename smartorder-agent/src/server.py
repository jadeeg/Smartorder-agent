import os
from pathlib import Path
from flask_cors import CORS

from flask import Flask, jsonify, request
import json

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "orders.json"


def load_orders():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"Orders file not found: {DATA_PATH}")
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON in {DATA_PATH}: {error}")


orders = load_orders()


@app.get("/orders/<order_id>")
def get_order(order_id):
    order = next(
        (order for order in orders if order["orderId"] == order_id),
        None,
    )
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)


@app.get("/orders")
def find_order():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    matching_orders = [
        order for order in orders
        if order["email"].lower() == email.lower()
    ]
    return jsonify(matching_orders)


@app.post("/chat")
def chat():
    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "response": "Please enter a message."
        }), 400

    # Temporary chatbot logic for testing React ↔ Flask
    if "12345" in message:
        order = next(
            (
                order for order in orders
                if order["orderId"] == "12345"
            ),
            None
        )

        if order:
            return jsonify({
                "response": (
                    f"Order #{order['orderId']} is currently "
                    f"{order['status']}. "
                    f"It is expected to arrive by "
                    f"{order['estimatedDelivery']}."
                )
            })

    return jsonify({
        "response": (
            "I can help with delivery tracking, "
            "order cancellation, cancellation policies, "
            "or connecting you with a support agent."
        )
    })

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

