import pytest
from day2 import addition, subtraction

def test_addition():
    assert addition(2, 3) == 5



def test_subtraction():
    assert subtraction(5, 3) == 2
