import requests

API_URL = "http://127.0.0.1:5000"


def get_order(order_id):
    response = requests.get(f"{API_URL}/orders/{order_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def check_delivery(order_id):
    order = get_order(order_id)
    if not order:
        return "I couldn't find the order with that number. Please try again"
    return (
        f"Order #{order['orderId']} is currently "
        f"{order['status']}. "
        f"It was shipped on {order['shippingDate']} "
        f"and is expected to arrive by "
        f"{order['estimatedDelivery']}."
    )


if __name__ == "__main__":
    print("SmartOrder Assistant")
    print("Please type 'exit' to quit")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.lower() == "exit":
            print("Thank you for using SmartOrder Assistant")
            break
        if user_input.isdigit():
            response = check_delivery(user_input)
            print("Agent:", response)
        else:
            print("Agent: Please enter your order number.")
