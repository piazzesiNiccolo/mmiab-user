from flask.signals import message_flashed
from mock.mock import patch, MagicMock, Mock
import pytest
import mock
import datetime
from mib import db
from mib.models.user import User
from mib.dao.user_manager import UserManager
from mib.dao.user_blacklist import UserBlacklist

@pytest.fixture
def mock_get_bl():
    with patch('mib.dao.user_blacklist.UserBlacklist._get_blacklist') as mock:
        yield mock

@pytest.fixture
def mock_set_bl():
    with patch('mib.dao.user_blacklist.UserBlacklist._set_blacklist') as mock:
        yield mock

class TestUserBlacklist:

    def test_blacklist_add_same_id_forbidden(self):
        code, message = UserBlacklist.add_user_to_blacklist(1,1)
        assert code == 403
        assert message == "Users cannot block themselves"

    def test_blacklist_add_blocking_does_not_exists(self):
        code, message = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 404
        assert message == "Blocking user not found"
    
    def test_blacklist_add_blocked_does_not_exists(self, users):
        code, message = UserBlacklist.add_user_to_blacklist(1,3)
        assert code == 404
        assert message == "Blocked user not found"
    
    def test_blacklist_add_user_already_blacklisted(self, mock_rbi, mock_set_bl, mock_get_bl):
        mock_rbi.return_value = 'ff'
        mock_get_bl.return_value = {2}
        code, message = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 200
        assert message == "User already in blacklist"

    def test_blacklist_add_user_ok(self, users):
        code, message = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 201
        assert message == "User added to blacklist"
        user, _ = users
        assert UserBlacklist._get_blacklist(user) == {2}
    
    def test_blacklist_remove_blocking_does_not_exists(self):
        code, message = UserBlacklist.remove_user_from_blacklist(1,2)
        assert code == 404
        assert message == "Blocking user not found"
    
    def test_blacklist_remove_blocked_does_not_exists(self, users):
        code, message = UserBlacklist.remove_user_from_blacklist(1,3)
        assert code == 404
        assert message == "Blocked user not found"
    
    def test_blacklist_remove_user_ok(self, users):
        code, message = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 201
        code, message = UserBlacklist.remove_user_from_blacklist(1,2)
        assert code == 200
        assert message == "User removed from blacklist"

    def test_blacklist_filter_empty(self, users):
        assert UserBlacklist.filter_blacklist(1, list(users)) == list(users)

    def test_blacklist_filter_ok(self, users):
        code, _ = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 201
        assert UserBlacklist.filter_blacklist(1, list(users)) == [users[0]]

    def test_blacklist_get_blocked(self, users):
        assert UserBlacklist.get_blocked_users(1) == []
        code, _ = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 201
        assert UserBlacklist.get_blocked_users(1) == [users[1]]
        code, _ = UserBlacklist.remove_user_from_blacklist(1,2)
        assert code == 200
        assert UserBlacklist.get_blocked_users(1) == []

    def test_blacklist_get_blocked_not_esisting_blocker(self):
        val, code, message = UserBlacklist.is_user_blocked(1, 2)
        assert val == False
        assert code == 404
        assert message == 'Blocking user not found'

    def test_blacklist_get_blocked_ok(self, users):
        assert UserBlacklist.is_user_blocked(1, 2) == (False, 200, 'State of blocked users')
        code, _ = UserBlacklist.add_user_to_blacklist(1,2)
        assert code == 201
        assert UserBlacklist.is_user_blocked(1, 2) == (True, 200, 'State of blocked users')
        code, _ = UserBlacklist.remove_user_from_blacklist(1,2)
        assert code == 200
        assert UserBlacklist.is_user_blocked(1, 2) == (False, 200, 'State of blocked users')





    
