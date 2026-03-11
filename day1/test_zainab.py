import pytest
from main import add_item, remove_item, get_total, apply_discount

# Fixtures
@pytest.fixture
def empty_cart():
    return []

@pytest.fixture
def loaded_cart():
    return [
        {"name": "Laptop", "price": 1000},
        {"name": "Mouse", "price": 50},
        {"name": "Keyboard", "price": 150},
    ]

# Adding
def test_add_single_item(empty_cart):
    add_item(empty_cart, "Phone", 500)
    assert len(empty_cart) == 1
    assert empty_cart[0]["name"] == "Phone"

def test_add_multiple_items(empty_cart):
    add_item(empty_cart, "A", 10)
    add_item(empty_cart, "B", 20)
    assert len(empty_cart) == 2

def test_add_item_price_check(empty_cart):
    add_item(empty_cart, "Book", 15)
    assert empty_cart[0]["price"] == 15

# Removing
def test_remove_existing_item(loaded_cart):
    remove_item(loaded_cart, "Mouse")
    assert len(loaded_cart) == 2
    assert all(item["name"] != "Mouse" for item in loaded_cart)

def test_remove_non_existent_item(loaded_cart):
    initial_len = len(loaded_cart)
    remove_item(loaded_cart, "Tablet")
    assert len(loaded_cart) == initial_len

# Total
def test_total_of_empty_cart(empty_cart):
    assert get_total(empty_cart) == 0

def test_total_of_loaded_cart(loaded_cart):
    assert get_total(loaded_cart) == 1200

# Discount
def test_apply_valid_discount():
    total = 100
    assert apply_discount(total, 10) == 90

def test_apply_zero_discount():
    total = 100
    assert apply_discount(total, 0) == 100

def test_apply_invalid_discount_raises_error():
    with pytest.raises(ValueError):
        apply_discount(100, 110)