from typing import Optional
import os, time
import threading
import logging
logger = logging.getLogger(__name__)
import requests
from app.message_exchange.rabbitmq import RabbitMQListener
import json
import datetime
from app.database.queries import insert_acknowledgement


class AbstractMessageQueueListener:
    def __init__(self, queue_name:str, routing_key:str, host="localhost"):
        self.host = host
        self.routing_key=routing_key
        self.queue = queue_name
        self.on_message_callback=self.message_callback
        self._reconnect_delay=0
        self.listener = RabbitMQListener(queue=queue_name,routing_key=routing_key, host=host, on_message_callback=self.on_message_callback)

    def run(self):
         while True:
            try:
                self.listener.run()
            except KeyboardInterrupt:
                self.listener.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self.listener.should_reconnect:
            self.listener.stop()
            reconnect_delay = self._get_reconnect_delay()
            #logger.info('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self.listener = RabbitMQListener(self.queue,self.routing_key, host=self.host, on_message_callback=self.on_message_callback)

    def _get_reconnect_delay(self):
        if self.listener.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay

    

    @staticmethod
    def message_callback(message):
        try:
            print(message)
            update_result = insert_acknowledgement(json.loads(message))
            logger.info("Reciveved | Message:{}|  Time:{}".format(json.loads(message),datetime.datetime.now()))
        except:
            logger.error("Error in message exchange")



class DBInsertListener:
    def __init__(self):
        self.listener = AbstractMessageQueueListener(queue_name="poc.db.output", routing_key="db.output", host=os.getenv("RABBITMQ_HOST","localhost"))
    
    def run(self):
        
        x = threading.Thread(target=self.listener.run, daemon=True)
        x.start()

dil = DBInsertListener()