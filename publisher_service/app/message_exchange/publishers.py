import os
import logging
import time
import functools
import datetime
import pika
import pytz

logger = logging.getLogger(__name__)

from app.message_exchange.rabbitmq import RabbitMQPublisher


class AbstractPublisher:
    def __init__(self, queue_name:str, routing_key:str, host="localhost") -> None:
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.host = host
        self._reconnect_delay=0
        self.publisher = RabbitMQPublisher(queue_name=self.queue_name, routing_key=self.routing_key, host=self.host)

    def run(self):
        while True:
            try:
                self.publisher.run()
            except KeyboardInterrupt:
                self.publisher.stop()
                break
            self._maybe_reconnect()
        logger.info("Thread stopped")
        

    def _maybe_reconnect(self):
        if self.publisher.should_reconnect:
            self.publisher.stop()
            reconnect_delay = self._get_reconnect_delay()
            logger.info('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self.publisher = RabbitMQPublisher(queue_name=self.queue_name, routing_key=self.routing_key, host=self.host)

    def _get_reconnect_delay(self):
        if self.publisher.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
    
    def publish(self, message:str):
        logger.info("Publishing message:{} on [{}] | Time:{}".format(message, self.queue_name,datetime.datetime.now()))
        self.publisher.publish(message)
        tz = pytz.timezone("Asia/Kolkata")
        return datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None)

class __ChatResponsePublisher(AbstractPublisher):
    def __init__(self) -> None:
        super().__init__(queue_name="poc.chat.output", routing_key="chat.output", host="localhost")

crp = __ChatResponsePublisher()

class __DBInsertPublisher(AbstractPublisher):
    def __init__(self) -> None:
        super().__init__(queue_name="poc.db.output", routing_key="db.output", host="localhost")

dbp = __DBInsertPublisher()

