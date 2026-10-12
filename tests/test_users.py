import pytest

from services.users import create_user, get_pref, get_user, update_pref
from utils.errors import NotFoundError, ValidationError


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

def test_get_pref_default():
    assert get_pref(1) == "none"

def test_get_pref_invalid_user():
    with pytest.raises(NotFoundError):
        get_pref(999)

@pytest.mark.parametrize("pref", ["email", "sms", "none"])
def test_update_pref_valid(pref):
    result = update_pref(1, pref)
    assert result["notification_pref"] == pref
    assert get_pref(1) == pref

def test_update_pref_invalid_pref():
    with pytest.raises(ValidationError) as exc_info:
        update_pref(1, "carrier_pigeon")
    assert exc_info.value.status_code == 422
    assert get_pref(1) == "none"

def test_update_pref_invalid_user():
    with pytest.raises(NotFoundError) as exc_info:
        update_pref(999, "email")
    assert exc_info.value.status_code == 404

@pytest.mark.parametrize("pref", ["email", "sms"])
def test_create_user_with_pref(pref):
    result = create_user("Dave", "dave@example.com", notification_pref=pref)
    assert result["notification_pref"] == pref
    assert get_user(result["id"])["notification_pref"] == pref
    assert get_pref(result["id"]) == pref

@pytest.mark.parametrize("pref", ["email", "sms"])
def test_get_user_after_pref_update(pref):
    update_pref(2, pref)
    result = get_user(2)
    assert result["name"] == "Bob"
    assert result["notification_pref"] == pref

def test_create_user_invalid_pref():
    with pytest.raises(ValidationError):
        create_user("Eve", "eve@example.com", notification_pref="fax")
