import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from mib import create_app
from mib.events.callbacks import update_points_to_users
from mib.events.channels import SUBSCRIBE_CHANNEL_POINTS_UPDATE
from mib.events.redis_setup import get_redis


class EventSubscribers:  # pragma: no cover
    @classmethod
    def points_updater(cls, app):
        redis_c = get_redis(app)
        p = redis_c.pubsub()
        p.subscribe(SUBSCRIBE_CHANNEL_POINTS_UPDATE)
        logging.debug(f"subscribed on channel {SUBSCRIBE_CHANNEL_POINTS_UPDATE}")
        for message in p.listen():
            with app.app_context():
                update_points_to_users(message)


event_subscribers = [{"subscriber": EventSubscribers.points_updater}]


def init_subscribers():  # pragma: no cover
    app = create_app()
    logging.info("setting up subscribers...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(sub["subscriber"], app) for sub in event_subscribers]
    wait(futures)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(init_subscribers())
