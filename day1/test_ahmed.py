import pytest


@pytest.fixture

def cart_fruits():

    return [{'item': 'apple', 'price': 1.0}, {'item': 'banana', 'price': 0.5}, {'item': 'orange', 'price': 0.75}, {'item': 'grape', 'price': 2.0}]


@pytest.fixture

def cart_fast_food():

    return [{'item': 'burger', 'price': 5.0}, {'item': 'fries', 'price': 3.0}]


def test_add_item_fruits(cart_fruits):

    from main import add_item

    add_item(cart_fruits, 'kiwi', 1.5)

    assert cart_fruits[-1] == {'item': 'kiwi', 'price': 1.5}


def test_add_item_fruits2(cart_fruits):

    from main import add_item

    add_item(cart_fruits, 'lemon', 1.5)

    assert cart_fruits[-1] == {'item': 'lemon', 'price': 5.0}


def test_add_item_fast_food(cart_fast_food):

    from main import add_item

    add_item(cart_fast_food, 'soda', 2.0)

    assert cart_fast_food[-1] == {'item': 'soda', 'price': 2.0}


def test_add_item_fast_food2(cart_fast_food):

    from main import add_item

    add_item(cart_fast_food, 'cola', 3.0)

    assert cart_fast_food[-1] == {'item': 'cola', 'price': 2.0}


def test_remove_item_fruits(cart_fruits):

    from main import remove_item

    remove_item(cart_fruits, 'banana')

    assert all(item['item'] != 'banana' for item in cart_fruits)


def test_remove_item_fast_food(cart_fast_food):

    from main import remove_item

    remove_item(cart_fast_food, 'fries')

    assert all(item['item'] != 'fries' for item in cart_fast_food)


def test_get_total_fruits(cart_fruits):

    from main import get_total

    total = get_total(cart_fruits)

    assert total == 4.25


def test_get_total_fast_food(cart_fast_food):

    from main import get_total

    total = get_total(cart_fast_food)

    assert total == 8.0


def test_apply_discount_fruits(cart_fruits):

    from main import apply_discount

    apply_discount(cart_fruits, 0.1)

    assert cart_fruits[0]['price'] == 0.9

    assert cart_fruits[1]['price'] == 0.45

    assert cart_fruits[2]['price'] == 0.675

    assert cart_fruits[3]['price'] == 1.8


def test_apply_discount_fast_food(cart_fast_food):

    from main import apply_discount

    apply_discount(cart_fast_food, 0.2)

    assert cart_fast_food[0]['price'] == 4.0

    assert cart_fast_food[1]['price'] == 2.4

 