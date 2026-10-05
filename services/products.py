from utils.errors import NotFoundError, ValidationError

PRODUCTS: dict[int, dict] = {
    1: {"id": 1, "name": "Notebook", "price": 4.99},
    2: {"id": 2, "name": "Pen",      "price": 1.49},
}

def get_product(product_id: int) -> dict:
    """Retrieve a product by ID.

    Args:
        product_id: The unique identifier for the product.

    Returns:
        The product record as a dictionary.

    Raises:
        NotFoundError: If no product exists with the given ID.
    """
    if product_id not in PRODUCTS:
        raise NotFoundError("Product")
    return PRODUCTS[product_id]

def create_product(name: str, price: float) -> dict:
    """Create a new product.

    Args:
        name: The product's display name.
        price: The product's price.

    Returns:
        The newly created product record.

    Raises:
        ValidationError: If name is empty or price is not a non-negative number.
    """
    if not name or not name.strip():
        raise ValidationError("name", "cannot be empty")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        raise ValidationError("price", "must be a non-negative number")
    new_id = max(PRODUCTS.keys()) + 1
    PRODUCTS[new_id] = {"id": new_id, "name": name, "price": price}
    return PRODUCTS[new_id]
