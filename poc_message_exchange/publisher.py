#!/usr/bin/env python

from random import random
import threading
import pika
import uuid
import queries
import time
import json
import random

def on_open(connection):
    connection.channel(on_open_callback = on_channel_open)
def on_channel_open(channel):
    channel.
#create a publisher
def createpublisher(queue_name,routing_key,publisher_number,counter):
    url = 'amqp://guest:guest@localhost:5672/%2F'
    connection = pika.SelectConnection(
            pika.URLParameters(url),
            on_open_callback=on_connection_open,
            on_close_callback=on_connection_closed,
            stop_ioloop_on_close=False)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue= queue_name)
    

    i=0
    while i<counter:   
        post_message = f"Hello Message Pub{publisher_number} {i+1}"
        is_unique=False
        while not is_unique:
            id = uuid.uuid1().hex
            is_unique = queries.check_unique_rabbit_id(id)
        
        msg = json.dumps({"message_id":id,"message":post_message},ensure_ascii=False)

        inserted_db= queries.insert_in_db(id,msg,f"publisher{publisher_number}")
        properties = pika.BasicProperties(
            app_id=f'publisher-{publisher_number}',
            content_type='application/json',
            delivery_mode=1)
        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body = msg,
            properties = properties
        )
        print(f"Published message Publisher-{publisher_number} {i+1}::{msg}")
        i=i+1
    connection.close()




def createpublisher2(counter):
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue= 'hello2')
    
    i=0
    while i<counter:   
        post_message = f"Hello Message Pub2 {i+1}"
        is_unique=False
        while not is_unique:
            id = uuid.uuid1().hex
            is_unique = queries.check_unique_rabbit_id(id)
        
        msg = json.dumps({"message_id":id,"message":post_message},ensure_ascii=False)

        inserted_db= queries.insert_in_db(id,msg,"publisher2")
        properties = pika.BasicProperties(
            app_id='publisher-2',
            content_type='application/json',
            delivery_mode=1)
        time.sleep(random.random)
        channel.basic_publish(
            exchange='',
            routing_key='hello2',
            body = msg,
            properties = properties
        )
        print(f"Published message Publisher 2 {i+1}::{msg}")
        i=i+1
    connection.close()

if __name__=="__main__":
    t1= threading.Thread(target=createpublisher,args=('hello','hello',1,10000))
    t1.start()
    t2= threading.Thread(target=createpublisher,args=('hello2','hello2',2,10000))
    t2.start()


    