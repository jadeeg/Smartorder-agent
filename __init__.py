from .tools import get_order, check_delivery


def register(ctx):
    ctx.register_tool(
        name="get_order",
        toolset="smartorder",
        schema={
            "name": "get_order",
            "description": "Retrieve a SmartOrder after verifying both order ID and customer email.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order number."
                    },
                    "email": {
                        "type": "string",
                        "description": "The customer's email address."
                    }
                },
                "required": ["order_id", "email"]
            }
        },
        handler=get_order
    )
    ctx.register_tool(
        name="check_delivery",
        toolset="smartorder",
        schema={
            "name": "check_delivery",
            "description": "Check where a SmartOrder is, its shipping status, and estimated delivery. Requires order ID and customer email.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order number."
                    },
                    "email": {
                        "type": "string",
                        "description": "The customer's email address."
                    }
                },
                "required": ["order_id", "email"]
            }
        },
        handler=check_delivery
    )
