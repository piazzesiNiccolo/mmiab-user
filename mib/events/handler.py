import logging
from mib.events import rabbit,disabled
from mib.events.event import Event
class EventHandler(object):

    @classmethod
    def send_event(cls, event: Event):
        if disabled:
            return None 
        else:
            logging.info(f"{event.key} triggered, sending message to broker")
            rabbit.send(
                body=event.body,
                key=event.key
            )
    
