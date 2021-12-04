import pytest

from mib.events.publishers import EventPublishers


class TestPublishers:
    @pytest.mark.parametrize("payload,ret", [({}, None), ({"user_id": 1}, 0)])
    def test_publish_user_delete(self, payload, ret):
        assert EventPublishers.publish_user_delete(payload) == ret
