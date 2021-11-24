from mib import db
from typing import List
from typing import Tuple
from typing import Set

from mib.models.user import User
from mib.dao.user_manager import UserManager

class UserBlacklist:

    __separator = "|"

    @staticmethod
    def _get_blacklist(current_user: User) -> Set[int]:
        if current_user.blacklist is None:
            return set()
        blocked_users = set(
            [
                int(user)
                for user in current_user.blacklist.split(UserBlacklist.__separator)
                if user.isdigit()
            ]
        )
        blocked_users.discard(current_user.id)
        return blocked_users

    def _set_blacklist(current_user: User, blocked_users: Set[int]) -> None:
        str_blocked_users = UserBlacklist.__separator.join(
            [str(user) for user in list(blocked_users)]
        )
        current_user.blacklist = str_blocked_users if str_blocked_users != "" else None
        db.session.commit()

    @staticmethod
    def add_user_to_blacklist(current_id: int, other_id: int) -> Tuple[int, str]:

        if current_id == other_id:
            return 403, "Users cannot block themselves"
        current_user = UserManager.retrieve_by_id(current_id)
        print(current_user)
        if current_user is None:
            return 404, "Blocking user not found"
        if UserManager.retrieve_by_id(other_id) is None:
            return 404, "Blocked user not found"

        code, message = 201, "User added to blacklist"

        blocked_users = UserBlacklist._get_blacklist(current_user)
        print(blocked_users, other_id)
        if other_id in blocked_users:
            code, message = 200, "User already in blacklist"
        blocked_users.add(other_id)
        UserBlacklist._set_blacklist(current_user, blocked_users)

        return code, message

    @staticmethod
    def remove_user_from_blacklist(current_id: int, other_id: int) -> Tuple[int, str]:
        current_user = UserManager.retrieve_by_id(current_id)
        if current_user is None:
            return 404, "Blocking user not found"
        if UserManager.retrieve_by_id(other_id) is None:
            return 404, "Blocked user not found"

        blocked_users = UserBlacklist._get_blacklist(current_user)
        blocked_users.discard(other_id)
        UserBlacklist._set_blacklist(current_user, blocked_users)

        return 200, "User removed from blacklist"

    @staticmethod
    def filter_blacklist(current_id: int, users: List[User]) -> List[User]:
        """
        Filters a list of User removing elements if they are on the blacklist
        of the specified user.
        """
        current_user = UserManager.retrieve_by_id(current_id)
        blocked_users = UserBlacklist._get_blacklist(current_user)
        return [user for user in users if user.id not in blocked_users]

    @staticmethod
    def get_blocked_users(current_id: int) -> List[User]:
        """
        Returns a list of blacklisted users
        """
        current_user = UserManager.retrieve_by_id(current_id)
        blocked_users = UserBlacklist._get_blacklist(current_user)
        return UserManager.retrieve_users_list(id_list=list(blocked_users), keep_empty=True)

    @staticmethod
    def is_user_blocked(current_id: int, other_id: int) -> Tuple[bool, int, str]:
        """
        Check if a user is in the blacklist of a given one.
        """
        current_user = UserManager.retrieve_by_id(current_id)
        if current_user is None:
            return False, 404, "Blocking user not found"
        return other_id in UserBlacklist._get_blacklist(current_user), 200, "State of blocked users"

