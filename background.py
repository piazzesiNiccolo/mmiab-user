from mib import create_app, create_celery
from kombu import Connection
from concurrent.futures import ThreadPoolExecutor
from mib.events.subscribers import subscribers

import logging
flask_app = create_app()
app = create_celery(flask_app)

def start_subscribers():
    with ThreadPoolExecutor(max_workers=8) as executor:
        for sub in subscribers:
            with Connection(app.config['RABMQ_RABBITMQ_URL'], heartbeat=4) as conn:
                worker = sub(conn, logging)
                executor.submit(worker.run)

if __name__ == "__main__":
    raise SystemExit(start_subscribers())