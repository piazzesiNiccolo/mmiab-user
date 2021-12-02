from mib import create_app, create_celery
from kombu import Connection
from concurrent.futures import ThreadPoolExecutor
from mib.events.subscribers import subscribers
import threading
import logging
flask_app = create_app()
app = create_celery(flask_app)

def start_subscribers():
        for sub in subscribers:
            with Connection(app.config['RABMQ_RABBITMQ_URL'], heartbeat=4) as conn:
                worker = sub(conn, logging)
                th = threading.Thread(target=worker.run)
                th.start()
                logging.info("Started new worker thread %s" % worker)

if __name__ == "__main__":
    raise SystemExit(start_subscribers())