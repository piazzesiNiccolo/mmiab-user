import pytest
import sqlalchemy 
from mib import db
from mib.models.user import User
from mib.dao.user_manager import UserManager
import datetime
class TestUserManager:

    def test_create_user_ok(self, test_client):
        user = User(
        first_name='Niccolò',
        last_name='Piazzesi',
        email='email@email.com',
        phone='38217192937',
        birthdate=datetime.datetime.strptime("01/01/2000","%d/%m/%Y")
        )
        UserManager.create_user(user)
        assert db.session.query(User).count() == 1
        db.session.delete(user)
        db.session.commit()
    
    