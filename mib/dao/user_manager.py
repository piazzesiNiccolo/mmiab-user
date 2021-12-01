from mib.dao.manager import Manager
from mib.models.user import User
from mib import db

from typing import List

class UserManager(Manager):
     
    
    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_, notme=0):
        Manager.check_none(id=id_)
        return User.query.filter(
            User.id == id_, 
            User.id != notme,
            User.is_banned == False,
        ).first()

    @staticmethod
    def retrieve_by_email(email, notme=0):
        return User.query.filter(
            User.email == email, 
            User.id != notme,
            User.is_banned == False,
        ).first()
    
    @staticmethod
    def retrieve_by_phone(phone, notme=0):
        Manager.check_none(phone=phone)
        return User.query.filter(
            User.phone == phone, 
            User.id != notme,
            User.is_banned == False,
        ).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)

    @staticmethod
    def set_content_filter(db_user: User):
        new_val = not db_user.content_filter
        db_user.content_filter = new_val
        db.session.commit()
        return new_val

    @staticmethod
    def retrieve_users_list(id_list : List[int] = [], keep_empty : bool = False) -> List[User]:
        if len(id_list) == 0:
            return [] if keep_empty else User.query.all()
        else:
            return User.query.filter(
                User.id.in_(id_list), 
                User.is_banned == False,
            ).all()

    @staticmethod
    def filter_users_by_keyword(users: List[User], key_word: str) -> List[User]:
        """
        Returns a list of users filtered by the presence of a key_word in one of
        the (relevant) columns in the database.
        """
        filter_users = lambda elem: (
            key_word in elem.first_name
            or key_word in elem.last_name
            or key_word in elem.email
            or (elem.nickname and key_word in elem.nickname)
            or (elem.location and key_word in elem.location)
        )

        if not key_word or key_word == "":
            return users

        filtered_users = list(filter(filter_users, users))
        return filtered_users if len(filtered_users) > 0 else users

