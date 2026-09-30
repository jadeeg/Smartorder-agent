import os
import json
import requests

from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

print("REQUESTS LOADED:", requests.__file__)



HERMES_URL = os.getenv(
    "HERMES_URL",
    "http://127.0.0.1:8642/v1/chat/completions",
)
HERMES_API_KEY = os.getenv(
    "HERMES_API_KEY",
    "smartorder-local-key"
)
app = Flask(__name__)
CORS(app)



BASE_DIR = Path(__file__).resolve().parent
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
    email = request.args.get("email", "").strip().lower()
    if not email:
        return jsonify({"error": "Email is required"}), 400

    order = next(
        (
            order for order in orders
            if order["orderId"] == order_id
            and order["email"].lower() == email
        ),
        None,
    )
    if not order:
        return jsonify({"error": "Order not found or verification failed"}), 404
    return jsonify(order)


@app.get("/orders")
def find_order():
    order_id = request.args.get("order_id", "").strip()
    email = request.args.get("email", "").strip().lower()
    if not order_id or not email:
        return jsonify({"error": "Order ID and email are required"}), 400

    order = next(
        (
            order for order in orders
            if order["orderId"] == order_id
            and order["email"].lower() == email
        ),
        None,
    )
    if not order:
        return jsonify({"error": "Order not found or verification failed"}), 404
    return jsonify(order)


@app.post("/chat")
def chat():
    try:
        data = request.get_json() or {}

        messages = data.get("messages", [])

        if not messages:
            return jsonify({
                "error": "Messages are required"
            }), 400

        response = requests.post(
            HERMES_URL,
            headers={
                "Authorization": f"Bearer {HERMES_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "hermes-agent",
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )

        print("Hermes status:", response.status_code)
        print("Hermes response:", response.text)

        response.raise_for_status()

        result = response.json()

        assistant_message = result["choices"][0]["message"]["content"]

        return jsonify({
            "response": assistant_message
        })

    except Exception as error:
        print("CHAT ERROR:", repr(error))

        return jsonify({
            "error": str(error)
        }), 500

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

