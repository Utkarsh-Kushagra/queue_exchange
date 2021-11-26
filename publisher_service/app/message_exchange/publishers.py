import os,sys
import logging
import time
import functools
import datetime
import pika
import pytz
import threading
import json

logger = logging.getLogger(__name__)

sys.path.append(os.path.realpath(os.path.relpath("../..")))
from app.message_exchange.rabbitmq import RabbitMQPublisher


class AbstractPublisher:
    def __init__(self, queue_name:str, routing_key:str, host="localhost") -> None:
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.host = host
        self._reconnect_delay=0
        self.publisher = RabbitMQPublisher(queue_name=self.queue_name, routing_key=self.routing_key, host=self.host)
        self.lock_thread = threading.Lock()
        #threading.Thread(target=self.publisher(queue_name=self.queue_name, routing_key=self.routing_key, host=self.host))

    def run(self):
        while True:
            try:
                print("Does it come here")
                self.publisher.run()
                print(self.publisher.run())
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
        print("Publishing message:{} on [{}] | Time:{}".format(message, self.queue_name,datetime.datetime.now()))
        self.publisher.publish(message)
        tz = pytz.timezone("Asia/Kolkata")
        
        return datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None)

class ChatResponsePublisher(AbstractPublisher):
    def __init__(self) -> None:
        super().__init__(queue_name="poc.chat.output", routing_key="chat.output", host=os.getenv("RABBITMQ_HOST","localhost"))

crp = ChatResponsePublisher()

class DBInsertPublisher(AbstractPublisher):
    def __init__(self) -> None:
        super().__init__(queue_name="poc.db.output", routing_key="db.output", host=os.getenv("RABBITMQ_HOST","localhost"))

dbp = DBInsertPublisher()



if __name__=="__main__":
    import threading
    dbp = DBInsertPublisher()
    z = threading.Thread(target=dbp.run, daemon=True)
    z.start()
    dbp.publisher.publish(json.dumps({'dbp_id': 'dbp_333c8fdb4b9311ec9532d5476e510adb', 'message': 'Thread :4 Message 97'}))
    

