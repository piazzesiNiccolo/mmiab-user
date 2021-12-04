import json
from mib.events.callbacks import update_points_to_users
import pytest
from mib import db
from mib.models import User
from datetime import datetime


class TestCallbacks:
    @pytest.mark.parametrize("type,points1,points2",[
        ("message",1,0),
        ("foo",0,0)
    ])
    def test_points_update(self,users,type,points1,points2):
        user = User.query.get(1)
        user2 = User.query.get(2)
        assert user.lottery_points == 0
        assert user2.lottery_points == 0
        payload = {
            "type": type,
            "data": json.dumps(
                {"users": [{"id": 1, "points": 1}, {"id": 2, "points": -1}]}
            ),
        }
        update_points_to_users(payload)
        assert user.lottery_points == points1
        assert user2.lottery_points == points2

   
