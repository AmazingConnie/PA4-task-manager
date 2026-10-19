import copy

import pytest

from services.products import PRODUCTS
from services.tags import TAGS
from services.tasks import TASKS
from services.users import USERS


@pytest.fixture(autouse=True)
def reset_data():
    """Restore the in-memory data stores after each test."""
    stores = [USERS, TASKS, PRODUCTS, TAGS]
    snapshots = [copy.deepcopy(store) for store in stores]
    yield
    for store, snapshot in zip(stores, snapshots):
        store.clear()
        store.update(snapshot)
