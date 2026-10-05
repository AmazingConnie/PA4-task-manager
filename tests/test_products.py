import pytest
from services.products import get_product, create_product

def test_get_product_valid():
    result = get_product(2)
    assert result["name"] == "Pen"

def test_get_product_invalid():
    with pytest.raises(Exception):
        get_product(999)

def test_create_product_valid():
    result = create_product("Stapler", 7.25)
    assert result["name"] == "Stapler"
    assert result["price"] == 7.25

def test_create_product_invalid():
    with pytest.raises(Exception):
        create_product("Eraser", -1)
