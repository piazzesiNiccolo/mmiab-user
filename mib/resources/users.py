from datetime import datetime

from flask import jsonify
from flask import request

from mib.dao.user_blacklist import UserBlacklist
from mib.dao.user_manager import UserManager
from mib.dao.user_reports import UserReport
from mib.dao.utils import Utils
from mib.models import User


def create_user():
    """This method allows the creation of a new user."""
    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")

    searched_user = UserManager.retrieve_by_email(email)
    if searched_user is not None:
        return (
            jsonify(
                {
                    "status": "Already present",
                    "message": "A user with this email is already registered",
                }
            ),
            200,
        )

    user = User()
    user.set_email(email)
    user.set_password(password)
    user.set_first_name(post_data.get("first_name"))
    user.set_last_name(post_data.get("last_name"))
    user.set_nickname(post_data.get("nickname"))
    user.set_location(post_data.get("location"))
    file_name = Utils.save_profile_picture(post_data.get("profile_picture"))
    user.set_pfp_path(file_name)
    user.set_birthday(
        datetime.strptime(
            post_data.get("birthdate"),
            "%d/%m/%Y",
        )
    )
    user.set_phone(post_data.get("phone"))
    UserManager.create_user(user)

    response_object = {
        "user": user.serialize(),
        "profile_picture": Utils.load_profile_picture(user),
        "status": "success",
        "message": "User successfully registered",
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
        response = {"status": "User not present"}
        return jsonify(response), 404

    return (
        jsonify(
            {
                "user": user.serialize(),
                "profile_picture": Utils.load_profile_picture(user),
            }
        ),
        200,
    )


def get_user_by_email(user_email):
    """
    Get a user by its current email.

    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {"status": "User not present"}
        return jsonify(response), 404

    return (
        jsonify(
            {
                "user": user.serialize(),
                "profile_picture": Utils.load_profile_picture(user),
            }
        ),
        200,
    )


def delete_user(user_id):
    """
    Delete the user with id = user_id.

    :param user_id the id of user to be deleted
    :return json response
    """
    if UserManager.retrieve_by_id(user_id) is None:
        response_object = {"status": "failed", "message": "User not found"}
        return jsonify(response_object), 404
    else:
        UserManager.delete_user_by_id(user_id)
        response_object = {
            "status": "success",
            "message": "Successfully deleted",
        }

        return jsonify(response_object), 202


def toggle_content_filter(id: int):
    """
    It enables the content filter option for a user if disabled
    and viceversa.
    """
    user = UserManager.retrieve_by_id(id)
    if user is None:
        response_object = {"status": "failed", "message": "User not found"}
        return jsonify(response_object), 404
    else:
        filter = UserManager.set_content_filter(user)
        response_object = {
            "status": "success",
            "message": "Content filter status changed",
            "value": filter,
        }
        return jsonify(response_object), 200


def get_users_toggle_content_filter(id_usr):

    toggle = UserManager.get_toggle_content_filter(id_usr)
    if toggle is None:
        response_object = {"status": "failed", "message": "not found"}
        return jsonify(response_object), 404
    else:
        response_object = {"status": "success", "toggle": toggle}
        return jsonify(response_object), 200


def get_users_list(id):
    if UserManager.retrieve_by_id(id) is None:
        response_object = {"status": "failed", "message": "not found"}
        return jsonify(response_object), 404
    else:
        key_word = request.args.get("q", default=None)
        users = UserManager.retrieve_users_list()
        valid_users = UserBlacklist.filter_blacklist(id, users)
        filtered_users = UserManager.filter_users_by_keyword(valid_users, key_word)

        response_object = {
            "status": "success",
            "users": [user.serialize() for user in filtered_users],
            "profile_pictures": [
                Utils.load_profile_picture(user) for user in filtered_users
            ],
        }
        return jsonify(response_object), 200


def get_blacklist(id):
    if UserManager.retrieve_by_id(id) is None:
        response_object = {"status": "failed", "message": "not found"}
        return jsonify(response_object), 404
    else:
        key_word = request.args.get("q", default=None)
        blocked_users = UserBlacklist.get_blocked_users(id)
        filtered_users = UserManager.filter_users_by_keyword(blocked_users, key_word)

        response_object = {
            "status": "success",
            "users": [user.serialize() for user in filtered_users],
            "profile_pictures": [
                Utils.load_profile_picture(user) for user in filtered_users
            ],
        }
        return jsonify(response_object), 200


def get_recipients(id):
    if UserManager.retrieve_by_id(id) is None:
        response_object = {"status": "failed", "message": "not found"}
        return jsonify(response_object), 404
    else:
        key_word = request.args.get("q", default=None)

        users = UserManager.retrieve_users_list()
        users = [u for u in users if u.id != id]
        valid_users = UserBlacklist.filter_blacklist(id, users)
        filtered_users = UserManager.filter_users_by_keyword(valid_users, key_word)

        response_object = {
            "status": "success",
            "users": [user.serialize_display() for user in filtered_users],
        }
        return jsonify(response_object), 200


def get_users_display_info():
    ids = request.args.get("ids", default='')

    ids_int = [int(id) for id in ids.split(',')]
    print(ids_int)
    users = UserManager.retrieve_users_list(
        id_list=ids_int,
        keep_empty=True,
    )

    response_object = {
        "status": "success",
        "users": [user.serialize_display() for user in users],
    }
    return jsonify(response_object), 200


def add_to_blacklist(blocking, blocked):
    code, message = UserBlacklist.add_user_to_blacklist(blocking, blocked)
    response_object = {
        "status": "success" if code == 201 else "failed",
        "message": message,
    }
    return jsonify(response_object), code


def remove_from_blacklist(blocking, blocked):
    code, message = UserBlacklist.remove_user_from_blacklist(blocking, blocked)
    response_object = {
        "status": "success" if code == 200 else "failed",
        "message": message,
    }
    return jsonify(response_object), code


def report(id_reporter: int, id_reported: int):
    code, message = UserReport.add_report(id_reported, id_reporter)
    response = {
        "status": "success" if code == 201 else "failed",
        "message": message,
    }
    print(response)
    return jsonify(response), code


def user_status(id, other):
    blocked = UserBlacklist.is_user_blocked(id, other)
    reported = UserReport.is_user_reported(id, other)

    response_object = {
        "status": "success",
        "blocked": blocked,
        "reported": reported,
    }
    return jsonify(response_object), 200


def update_user(user_id):
    data = request.get_json()
    user = UserManager.retrieve_by_id(user_id)

    if user is None:
        return (
            jsonify(
                {
                    "status": "failed",
                    "message": "User not found",
                }
            ),
            404,
        )
    new_mail = data.get("email")
    new_mail = None if new_mail == "" else new_mail
    new_phone = data.get("phone")
    new_phone = None if new_phone == "" else new_phone
    if (
        new_mail
        and UserManager.retrieve_by_email(data.get("email"), notme=user_id) is not None
    ):
        return jsonify({"status": "failed", "message": "Email already used"}), 400
    if (
        new_phone
        and UserManager.retrieve_by_phone(data.get("phone"), notme=user_id) is not None
    ):
        return jsonify({"status": "failed", "message": "Phone already used"}), 400

    old_password = data.get("old_password")
    old_password = None if old_password == "" else old_password
    new_password = data.get("new_password")
    new_password = None if new_password == "" else new_password

    if not old_password or not user.check_password(old_password):
        return jsonify({"status": "failed", "message": "Password incorrect"}), 200

    if new_password:
        user.set_password(new_password)

    propic = data.get("profile_picture")
    print(propic)
    if propic == "" or not propic:
        file_name = ""
    else:
        file_name = Utils.save_profile_picture(propic)

    user.set_email(data.get("email"))
    user.set_first_name(data.get("first_name"))
    user.set_last_name(data.get("last_name"))
    user.set_nickname(data.get("nickname"))
    user.set_location(data.get("location"))
    user.set_pfp_path(file_name)
    if data.get("birthdate"):
        user.set_birthday(
            datetime.strptime(
                data.get("birthdate"),
                "%d/%m/%Y",
            )
        )
    user.set_phone(data.get("phone"))

    UserManager.update_user(user)

    response_object = {
        "status": "success",
        "message": "User profile succesfully updated",
        "profile_picture": Utils.load_profile_picture(user),
    }
    return jsonify(response_object), 201
