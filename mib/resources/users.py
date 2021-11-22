from flask import request, jsonify
from mib.dao.user_manager import UserManager
from mib.models.user import User
from datetime import datetime


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

def get_users_list():
    key_word = request.args.get('q',default=None)

    users = UserManager.retrieve_users_list()

    filter_users = lambda elem: (
            key_word in elem.first_name
            or key_word in elem.last_name
            or key_word in elem.email
            or key_word in elem.phone
            or (elem.nickname and key_word in elem.nickname)
            or (elem.location and key_word in elem.location)
            
        )
    filtered_users = list(filter(filter_users, users))
    filtered_users = filtered_users if len(filtered_users) > 0 else users

    response_object = {
        'status': 'success',
        'users': [user.serialize() for user in users],
    }
    return jsonify(response_object), 200 


