def validate_quantity(quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive.")
    return quantity

def pretty_print_order(order):
    print("\n--- Order Summary ---")
    for k, v in order.items():
        print(f"{k}: {v}")
