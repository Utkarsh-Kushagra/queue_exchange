"""
Build an api which will tell parameters on how to run a task
Once we get the thread parameters we will spawn as many threads to send the message and see if it works
"""
import sys
import os
import logging
import json

sys.path.append(os.path.realpath(os.path.relpath("../..")))

logger = logging.getLogger(__name__)
import threading
import uuid
from app.database import queries

from app.model.database import SessionLocal
from sqlalchemy.orm import Session as DBSession
from app.model.database import get_db
from fastapi.param_functions import Depends
import pytz
from queue import Queue

from threading import Thread as Thread
import datetime
#import time
from time import sleep
thread_lock = threading.Lock()

from app.message_exchange.publishers import crp as  ChatResponsePublisher
from app.message_exchange.publishers import dbp as DBInsertPublisher

class ThreadTask:
    
    def __init__(self, worker_id):
        self._running = True
        self.msg = None
        self.conversation_id = worker_id

    def run_medication_task(self,worker,message):
        worker.publish_message(json.dumps({"conversation_id":worker.worker_id,"response":worker.name}))

class AbstractWorker:
    def __init__(self,worker_id) -> None:
        self.worker_id = worker_id
        self.database_publisher = DBInsertPublisher
        self.chat_publisher = ChatResponsePublisher

class MyWorker(AbstractWorker):


    def __init__(self,worker_id, name):
        super().__init__(worker_id)
        
        self.name = name

        #self.run()
        
    
    
    def run(self): 
        
        thread_task = ThreadTask(self.worker_id)
        t = threading.Thread(target=thread_task.run_medication_task,args=(self,self.worker_id),daemon=True)
        t.run()
        print(t.name)
        
    #this function is the wrapper publisher code. Here we publish and as well insert in DB.
    # Acquire lock here   
    def publish_message(self,message):
        thread_id = threading.get_ident()
        logger.critical(f"*********Acquired lock for Chat thread {thread_id} and message:: {message}***********")
        self.chat_publisher.lock_thread.acquire(1)
        
        db_session = SessionLocal()
        #lock_thread.acquire(1)
        
        is_unique=False
        while not is_unique:
            id = uuid.uuid1().hex
            is_unique = queries.check_unique_rabbit_id(id)
        
        tz="Asia/Kolkata"
        crp_id = "crp_"+id
        dbp_id = "dbp_"+id
        message_for_chat_listener = {"crp_id":crp_id,"message":message}
        
        time_publish = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S.%f")
        is_inserted = queries.create_update_rabbit_message_entry(crp_id,message_for_chat_listener,time_publish,None,"publisher-chat-response",None)
        logger.info("Insert Status:{}".format(is_inserted))

        self.chat_publisher.publish(json.dumps(message_for_chat_listener))
        logger.info(f'MESSAGE PUBLISHED  in Chat Queue:: {message_for_chat_listener}')
        self.chat_publisher.lock_thread.release()
        logger.critical(f"*********Release lock for Chat thread {thread_id} and message:: {message}***********")
        logger.critical(f"*********Acquiring lock for Database thread {thread_id} and message:: {message}***********")
        
        self.database_publisher.lock_thread.acquire(1)
        message_for_db_listener = {"dbp_id":dbp_id,"message":message}
        
        is_inserted = queries.create_update_rabbit_message_entry(dbp_id,message_for_db_listener,time_publish,None,"publisher-db-insert",None)
        self.database_publisher.publish(json.dumps(message_for_db_listener))
        logger.info(f'MESSAGE PUBLISHED  in DB Queue:: {message_for_db_listener}')
        #lock_thread.release()
        self.database_publisher.lock_thread.release()
        logger.critical(f"*********Release lock for Database thread {thread_id} and message:: {message}***********")
        return True

#replicates conversation engine. Create threads as provided in run_test.py
#create 15 threads and keep in a list in memory. Keep sending messages
def create_message(num_of_workers):

    print(f"Num of Conversation Objects Needed:{num_of_workers}")

    workerList = []
    for i in range (int(num_of_workers)):
      
        worker = MyWorker(i,f"Worker :{i+1} ")
        workerList.append(worker)
    for j in range(10):
        for worker in workerList:
            worker.run()
        sleep(2)
        logger.info(f"Done for cycle :{j}")
                


if __name__=="__main__":
    create_message(100)

