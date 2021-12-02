
from typing import Dict, NamedTuple

class Event(NamedTuple):
    key: str
    body: Dict


def user_delete_event(user_id: int):
    return Event("USER_DELETE",{"user_id": user_id})

