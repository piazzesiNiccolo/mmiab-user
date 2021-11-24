from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.dao.user_blacklist import UserBlacklist
from mib.models.user import User
from datetime import datetime
from mib import db


def create_user():
    """This method allows the creation of a new user.
    """
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return jsonify({
            'status': 'Already present'
        }), 200

    user = User()
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get('first_name'))
    user.set_last_name(post_data.get('last_name'))
    user.set_nickname(post_data.get('nickname'))
    user.set_location(post_data.get('location'))
    user.set_pfp_path(post_data.get('profile_picture'))
    user.set_birthday(
        datetime.strptime(
            post_data.get('birthdate'),
            '%d/%m/%Y',
        )
    )
    user.set_phone(post_data.get('phone'))
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return jsonify(response_object), 201

def get_user(user_id):
    """
    Get a user by its current id.

    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_user_by_email(user_email):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def delete_user(user_id):
    """
    Delete the user with id = user_id.

    :param user_id the id of user to be deleted
    :return json response
    """
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202

def toggle_content_filter(id: int):
        """
        It enables the content filter option for a user if disabled
        and viceversa.
        """
        db_user = db.session.query(User).filter(User.id == id)
        if db_user.count() == 0:
            response_object = {
            'status': 'failed',
            'Message': "User not found",
            }
            return jsonify(response_object), 404

        new_val = not db_user.first().content_filter
        db_user.update({User.content_filter: new_val})
        db.session.commit()

        response_object = {
            'status': 'Success',
            'Message': "Content filter status changed",
            }
        return jsonify(response_object), 404



def get_users_list(id):

    key_word = request.args.get('q',default=None)

    users = UserManager.retrieve_users_list()
    valid_users = UserBlacklist.filter_blacklist(id, users)
    filtered_users = UserManager.filter_users_by_keyword(valid_users, key_word)

    response_object = {
        'status': 'success',
        'users': [user.serialize() for user in filtered_users],
    }
    return jsonify(response_object), 200 

def get_blacklist(id):
    key_word = request.args.get('q',default=None)

    blocked_users = UserBlacklist.get_blocked_users(id)
    print('blocked', blocked_users)
    filtered_users = UserManager.filter_users_by_keyword(blocked_users, key_word)
    print('filtered', filtered_users)

    response_object = {
        'status': 'success',
        'users': [user.serialize() for user in filtered_users],
    }
    return jsonify(response_object), 200 

def add_to_blacklist(blocking, blocked):
    code, message = UserBlacklist.add_user_to_blacklist(blocking, blocked)
    response_object = { 
        'status': 'success' if code == 201 else 'failed',
        'message': message
    }
    return jsonify(response_object), code

def remove_from_blacklist(blocking, blocked):
    code, message = UserBlacklist.remove_user_from_blacklist(blocking, blocked)
    response_object = { 
        'status': 'success' if code == 202 else 'failed',
        'message': message
    }
    return jsonify(response_object), code

def is_blocked(blocking, blocked):
    val, code, message = UserBlacklist.is_user_blocked(blocking, blocked)
    response_object = { 
        'status': 'success' if code == 200 else 'failed',
        'message': message,
        'blocked': val
    }
    return jsonify(response_object), code

