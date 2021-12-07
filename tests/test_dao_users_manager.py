import datetime

import pytest

from mib import db
from mib.dao.user_manager import UserManager
from mib.models.user import User


class TestUserManager:
    def test_create_user_ok(self):
        user = User(
            first_name="Niccolò",
            last_name="Piazzesi",
            email="email@email.com",
            phone="38217192937",
            birthdate=datetime.datetime.strptime("01/01/2000", "%d/%m/%Y"),
        )
        UserManager.create_user(user)
        assert db.session.query(User).count() == 1
        db.session.delete(user)
        db.session.commit()

    def test_retrieve_by_id_None(self):

        assert UserManager.retrieve_by_id(1) is None

    @pytest.mark.parametrize(
        "id, email", [(1, "email@email.com"), (2, "email1@email1.com")]
    )
    def test_retrieve_by_id_exists(self, users, id, email):
        user = UserManager.retrieve_by_id(id)
        assert user.email == email

    def test_retrieve_by_email_None(self):
        assert UserManager.retrieve_by_email("email@email.com") is None

    @pytest.mark.parametrize(
        "email, phone",
        [("email@email.com", "38217192937"), ("email1@email1.com", "1234567890")],
    )
    def test_retrieve_by_email_exists(self, users, email, phone):
        user = UserManager.retrieve_by_email(email)
        assert user.phone == phone

    def test_retrieve_by_phone_None(self):
        assert UserManager.retrieve_by_phone("1234567890") is None

    @pytest.mark.parametrize(
        "email, phone",
        [("email@email.com", "38217192937"), ("email1@email1.com", "1234567890")],
    )
    def test_retrieve_by_phone_exists(self, users, email, phone):
        user = UserManager.retrieve_by_phone(phone)
        assert user.email == email

    def test_update_user(self, users):
        user = users[0]
        user.set_email("newmail@mail.com")
        UserManager.update_user(user)
        assert User.query.get(1).email == "newmail@mail.com"

    def test_delete_user(self):
        user = User(
            email="ex@ex.com",
            first_name="Niccolò",
            last_name="Piazzesi",
            phone="38217192937",
            birthdate=datetime.datetime.strptime("01/01/2000", "%d/%m/%Y"),
        )
        db.session.add(user)
        db.session.commit()
        UserManager.delete_user(user)
        assert User.query.get(1) is None

    def test_delete_user_by_id_None(self):
        with pytest.raises(ValueError):
            UserManager.delete_user_by_id(1)

    def test_delete_user_by_id(self):
        user = User(
            email="ex@ex.com",
            first_name="Niccolò",
            last_name="Piazzesi",
            phone="38217192937",
            birthdate=datetime.datetime.strptime("01/01/2000", "%d/%m/%Y"),
        )
        db.session.add(user)
        db.session.commit()
        UserManager.delete_user_by_id(1)
        assert User.query.get(1) is None

    def test_get_content_filter(self, users):
        assert not UserManager.get_toggle_content_filter(1)

    def test_set_content_filter_user_not_exists(self):
        cf = UserManager.set_content_filter(None)
        assert cf == False

    @pytest.mark.parametrize("cf_value", [True, False])
    def test_set_content_filter(self, users, cf_value):
        usr, _ = users
        usr.content_filter = cf_value
        UserManager.set_content_filter(usr)
        assert not usr.content_filter == cf_value

    @pytest.mark.parametrize("choice, length", [(True, 0), (False, 2)])
    def test_retrieve_users_choose_if_empty(self, users, length, choice):
        assert len(UserManager.retrieve_users_list(keep_empty=choice)) == length

    def test_retrieve_users(self, users):
        assert len(UserManager.retrieve_users_list(id_list=[1, 2])) == 2

    @pytest.mark.parametrize(
        "keyword, length",
        [("Faella", 2), ("Lorenzo", 1), ("Marco", 2), ("", 2), (None, 2)],
    )
    def test_filter_by_keword(self, users, keyword, length):
        assert (
            len(UserManager.filter_users_by_keyword(users, key_word=keyword)) == length
        )
