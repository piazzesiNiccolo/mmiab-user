import json
import logging
from mib import db
from mib.dao.user_manager import UserManager
from mib.models.user import User


def update_points_to_users(message):
    if message["type"] == "message":
        users = json.loads(message["data"])["users"]
        ids = list(map(lambda u: u.get("id"), users))
        print(ids)
        users_db = db.session.query(User).filter(User.id.in_(ids)).all()
        users_db = {u.id:u for u in users_db}
        for user in users:
            u = users_db[user["id"]]
            u.lottery_points += user["points"]
            if u.lottery_points < 0:
                u.lottery_points = 0
        UserManager.update()
