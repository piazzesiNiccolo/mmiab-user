import json
from typing import Dict

from flask import current_app

from mib.events.channels import PUBLISH_CHANNEL_USER_DELETE
from mib.events.redis_setup import get_redis


class EventPublishers:
    @classmethod
    def publish_user_delete(self, msg: Dict):
        if "user_id" not in msg:
            return None
        else:
            return get_redis(current_app).publish(
                PUBLISH_CHANNEL_USER_DELETE, json.dumps(msg)
            )
