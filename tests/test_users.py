import pytest
from services.users import get_user, create_user

def test_get_user_valid():
    result = get_user(1)
    assert result["name"] == "Alice"

def test_get_user_invalid():
    with pytest.raises(Exception):
        get_user(999)

def test_create_user_valid():
    result = create_user("Carol", "carol@example.com")
    assert result["name"] == "Carol"
    assert result["email"] == "carol@example.com"

def test_create_user_invalid():
    with pytest.raises(Exception):
        create_user("", "nobody@example.com")
