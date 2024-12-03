import os

import pytest
from tests.test_db import get_db

os.environ['TEST_ENV'] = 'True'

@pytest.fixture(scope="function")
def db_session():

    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
