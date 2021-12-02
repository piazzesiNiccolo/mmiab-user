from kombu.mixins import ConsumerMixin
from kombu import Exchange,Queue
from mib import api_app as app
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
        # send ack to message
        message.ack()        

    def get_consumers(self, consumer, channel):
        return [consumer(queues=self.queues,
                         callbacks=[self.on_message])]