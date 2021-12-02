from kombu.mixins import ConsumerMixin
from kombu import Exchange,Queue
from mib import api_app as app
from mib import db
from mib.dao.user_manager import UserManager
from mib.dao.manager import Manager
import json
class LotteryPointsUpdater(ConsumerMixin):

    def __init__(self, connection, logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger 
        exchange = Exchange(
            app.config.get('RABMQ_SEND_EXCHANGE_NAME'),
            type='topic',
            channel=connection.channel()
        )
        exchange.declare()
        self.queues = [Queue("LotteryUpdateQueue",exchange,routing_key="LOTTERY_UPDATE")]
    
    def on_message(self, body, message):
        obj = None
        try:
            obj = json.loads(body)
        except ValueError:
            self.logger.error('Cannot decode json message! Message=%s' % body)
            message.ack()
            return
        else:
            if 'winners' not in obj:
                self.logger.error('Message does not contain winners key!')
            else:
            # send ack to message
                for id,points in obj["winners"].items():
                    user = UserManager.retrieve_by_id(id)
                    user.lottery_points += points
                Manager.update()
            message.ack()  

    def get_consumers(self, consumer, channel):
        return [consumer(queues=self.queues,
                         callbacks=[self.on_message])]