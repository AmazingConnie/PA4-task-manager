import pytest

from app import app
from services.tags import TAGS, create_tag
from utils.errors import ValidationError


@pytest.fixture
def client():
    return app.test_client()

def test_create_tag_valid():
    result = create_tag("urgent")
    assert result["name"] == "urgent"
    assert TAGS[result["id"]] == result

@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_create_tag_invalid(name):
    with pytest.raises(ValidationError) as exc_info:
        create_tag(name)
    assert exc_info.value.status_code == 422

def test_create_tag_route_valid(client):
    response = client.post("/api/tags", json={"name": "urgent"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "urgent"

def test_create_tag_route_invalid(client):
    response = client.post("/api/tags", json={"name": ""})
    assert response.status_code == 422
