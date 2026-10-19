from utils.errors import ValidationError

TAGS: dict[int, dict] = {
    1: {"id": 1, "name": "work"},
    2: {"id": 2, "name": "personal"},
}

def create_tag(name: str) -> dict:
    """Create a new tag.

    Args:
        name: The tag's display name.

    Returns:
        The newly created tag record.

    Raises:
        ValidationError: If name is not a string or is empty.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("name", "cannot be empty")
    new_id = max(TAGS.keys()) + 1
    TAGS[new_id] = {"id": new_id, "name": name}
    return TAGS[new_id]
