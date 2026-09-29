import requests

API_URL = "https://smartorder-agent.onrender.com"


def get_order(order_id, email):
    response = requests.get(
        f"{API_URL}/customer/orders/{order_id}",
        params={"email": email},
        timeout=10,
    )
    if response.status_code == 404:
        return {"error": "Order not found"}
    response.raise_for_status()
    return response.json()


def check_delivery(order_id, email):
    try:
        order = get_order(order_id, email)
    except requests.exceptions.RequestException:
        return "I'm having trouble reaching the order system. Please try again later."

    if "error" in order:
        return "I couldn't find the order with that number. Please try again."

    status = order["status"]
    shipped = order["shippingDate"]
    estimated = order["estimatedDelivery"]

    if status == "shipped" and shipped:
        return (
            f"Order #{order['orderId']} is currently {status}. "
            f"It was shipped on {shipped} "
            f"and is expected to arrive by {estimated}."
        )
    elif status == "shipped":
        return (
            f"Order #{order['orderId']} is currently {status} "
            f"and is expected to arrive by {estimated}."
        )
    else:
        return (
            f"Order #{order['orderId']} is currently {status} "
            f"and is expected to arrive by {estimated}."
        )


if __name__ == "__main__":
    print("SmartOrder Assistant")
    print("Please type 'exit' to quit")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Thank you for using SmartOrder Assistant")
            break

        if user_input.isdigit():
            email = input("Enter your email: ")
            response = check_delivery(user_input, email)
            print("Agent:", response)
        else:
            print("Agent: Please enter your order number.")
