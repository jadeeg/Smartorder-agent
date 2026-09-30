from .tools import check_delivery, get_order


def register(ctx):
    order_parameters = {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The customer's order number.",
            },
            "email": {
                "type": "string",
                "description": "The email address used for the order.",
            },
        },
        "required": ["order_id", "email"],
    }

    ctx.register_tool(
        name="get_order",
        toolset="smartorder",
        schema={
            "name": "get_order",
            "description": "Retrieve a SmartOrder after verifying its number and customer email.",
            "input_schema": order_parameters,
        },
        handler=get_order,
    )
    ctx.register_tool(
        name="check_delivery",
        toolset="smartorder",
        schema={
            "name": "check_delivery",
            "description": "Check a SmartOrder's shipping status and estimated delivery after verifying its number and email.",
            "input_schema": order_parameters,
        },
        handler=check_delivery,
    )