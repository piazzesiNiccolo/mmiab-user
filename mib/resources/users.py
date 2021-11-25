from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.dao.user_blacklist import UserBlacklist
from mib.dao.user_reports import UserReport
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
    if UserManager.retrieve_by_id(id) is None:
        response_object = {
            'status': "failed",
            "message":"User not found"
        }
        return jsonify(response_object),404
    else:
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
        filter = UserManager.set_content_filter(id)
        
        if filter == -1:
            response_object = {
            'status': 'failed',
            'Message': "User not found",
            }
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'Success',
                'Message': "Content filter status changed",
                'Value': filter,
                }
            return jsonify(response_object), 200



def get_users_list(id):
    if UserManager.retrieve_by_id(id) is None:
        response_object = {
            "status":"failed",
            "message":"not found"
        }
        return jsonify(response_object),404
    else:
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
    filtered_users = UserManager.filter_users_by_keyword(blocked_users, key_word)

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
        'status': 'success' if code == 200 else 'failed',
        'message': message
    }
    return jsonify(response_object), code

def report(id_reporter: int, id_reported: int):
    code, message = UserReport.add_report(id_reported,id_reporter)
    response = {
        'status' : 'success' if code == 201 else 'failed',
        'message' : message,
    }
    print(response)
    return jsonify(response), code

def user_status(id, other):
    blocked = UserBlacklist.is_user_blocked(id, other)
    reported = UserReport.is_user_reported(id, other)

    response_object = { 
        'status': 'success',
        'blocked': blocked,
        'reported': reported,
    }
    return jsonify(response_object), 200

def update_user(user_id):
    data = request.get_json()
    user = UserManager.retrieve_by_id(user_id)

    if user is None:
        return jsonify({
            "status":"failed",
            'message': 'User not found'
        }), 404
    if data.get("phone") and UserManager.retrieve_by_phone(phone=data["phone"]) is not None:
        return jsonify({
            "status":"failed",
            'message': "Phone already used"

        }), 400
    if data.get("email") and UserManager.retrieve_by_email(email=data["email"]) is not None:
        return jsonify({
            "status":"failed",
            'message': "Email already used"
        }),400
    if data.get("old_password") and not user.check_password(data["old_password"]):
        return jsonify({
                "status":"failed",
                'message': 'Password incorrect'
        }), 200

    if data.get("new_password"):
        user.set_password(data["new_password"])

    user.set_email(data.get("email"))
    user.set_first_name(data.get('first_name'))
    user.set_last_name(data.get('last_name'))
    user.set_nickname(data.get('nickname'))
    user.set_location(data.get('location'))
    user.set_pfp_path(data.get('profile_picture'))
    if data.get("birthdate"):
        user.set_birthday(
            datetime.strptime(
                data.get('birthdate'),
                '%d/%m/%Y',
            )
        )
    user.set_phone(data.get('phone'))

    UserManager.update_user(user)

    response_object = {
        'status': 'success'
    }
    return jsonify(response_object), 201

