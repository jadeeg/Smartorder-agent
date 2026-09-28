import requests

API_URL = "http://127.0.0.1:5000"


def get_order(order_id, email):
    """Retrieve an order after verifying its ID against the customer's email."""
    response = requests.get(
        f"{API_URL}/customer/orders/{order_id}",
        params={"email": email},
        timeout=10,
    )
    if response.status_code == 404:
        return {"error": "Order not found or verification failed"}
    response.raise_for_status()
    return response.json()


def check_delivery(order_id, email):
    """Check delivery status for an order."""
    order = get_order(order_id, email)

    if "error" in order:
        return "I couldn't find the order with that number. Please try again."

    message = f"Order #{order['orderId']} is currently {order['status']}."
    if order.get("shippingDate"):
        message += f" It was shipped on {order['shippingDate']}."
    if order.get("estimatedDelivery"):
        message += f" It is expected to arrive by {order['estimatedDelivery']}."
    return message
