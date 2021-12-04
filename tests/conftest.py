from datetime import datetime

import pytest
from mock.mock import patch

from mib import create_app
from mib import db
from mib.models.user import User


@pytest.fixture(scope="session", autouse=True)
def test_client():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_rbi():
    with patch("mib.dao.user_manager.UserManager.retrieve_by_id") as mock:
        yield mock


@pytest.fixture
def mock_rbe():
    with patch("mib.dao.user_manager.UserManager.retrieve_by_email") as mock:
        yield mock


@pytest.fixture
def mock_rbp():
    with patch("mib.dao.user_manager.UserManager.retrieve_by_phone") as mock:
        yield mock


@pytest.fixture
def users():
    user = User(
        first_name="Niccolò",
        last_name="Piazzesi",
        email="email@email.com",
        phone="38217192937",
        birthdate=datetime.strptime("01/01/2000", "%d/%m/%Y"),
        location="Faella",
    )
    user.set_password("pass")
    user2 = User(
        first_name="Lorenzo",
        last_name="Volpi",
        email="email1@email1.com",
        phone="1234567890",
        birthdate=datetime.strptime("01/01/2000", "%d/%m/%Y"),
        location="Faella",
    )
    user2.set_password("pass")

    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    yield user, user2
    db.session.delete(user)
    db.session.delete(user2)
    db.session.commit()
