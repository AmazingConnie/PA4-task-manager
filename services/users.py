from utils.errors import NotFoundError, ValidationError

NOTIFICATION_PREFS: tuple[str, ...] = ("email", "sms", "none")

USERS: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "notification_pref": "none"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "notification_pref": "none"},
}

def get_user(user_id: int) -> dict:
    """Retrieve a user by ID.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        The user record as a dictionary.

    Raises:
        NotFoundError: If no user exists with the given ID.
    """
    if user_id not in USERS:
        raise NotFoundError("User")
    return USERS[user_id]

def create_user(name: str, email: str, notification_pref: str = "none") -> dict:
    """Create a new user.

    Args:
        name: The user's display name.
        email: The user's email address.
        notification_pref: How the user wants to be notified; one of
            'email', 'sms', or 'none'. Defaults to 'none'.

    Returns:
        The newly created user record.

    Raises:
        ValidationError: If name or email is empty, or notification_pref is
            not one of 'email', 'sms', or 'none'.
    """
    if not name or not name.strip():
        raise ValidationError("name", "cannot be empty")
    if not email or "@" not in email:
        raise ValidationError("email", "must be a valid email address")
    if notification_pref not in NOTIFICATION_PREFS:
        raise ValidationError("notification_pref", "must be one of 'email', 'sms', or 'none'")
    new_id = max(USERS.keys()) + 1
    USERS[new_id] = {"id": new_id, "name": name, "email": email,
                     "notification_pref": notification_pref}
    return USERS[new_id]

def get_pref(user_id: int) -> str:
    """Retrieve a user's notification preference.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        The user's current notification preference: 'email', 'sms', or 'none'.

    Raises:
        NotFoundError: If no user exists with the given ID.
    """
    if user_id not in USERS:
        raise NotFoundError("User")
    return USERS[user_id]["notification_pref"]

def update_pref(user_id: int, notification_pref: str) -> dict:
    """Update a user's notification preference.

    Args:
        user_id: The unique identifier for the user.
        notification_pref: The new preference; one of 'email', 'sms', or 'none'.

    Returns:
        The updated user record.

    Raises:
        NotFoundError: If no user exists with the given ID.
        ValidationError: If notification_pref is not one of 'email', 'sms',
            or 'none'.
    """
    if user_id not in USERS:
        raise NotFoundError("User")
    if notification_pref not in NOTIFICATION_PREFS:
        raise ValidationError("notification_pref", "must be one of 'email', 'sms', or 'none'")
    user = USERS[user_id]
    user["notification_pref"] = notification_pref
    return user
