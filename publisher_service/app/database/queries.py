import sys
import os
import uuid

from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.sqltypes import Time
from pathlib import Path
sys.path.append(os.path.realpath(os.path.relpath("../..")))
from dotenv import load_dotenv
load_dotenv(Path(os.path.realpath(os.path.relpath("..")))/"dev.env")
import requests

import json
import logging
from typing import List
logger = logging.getLogger(__name__)




from sqlalchemy.orm import Session as DBSession, query_expression, relation

from app.model import models
from sqlalchemy import desc, func,distinct
import datetime
from datetime import date, timedelta
import os
from app.model.database import SessionLocal
from app.model.database import get_db

# from app.message_exchange.publishers import crp as ChatResponsePublisher
# from app.message_exchange.publishers import dbp as DBInsertPublisher

#from app.worker import worker
import pprint

import shutil
from os import name, path
from sqlalchemy import func

from fastapi.responses import FileResponse
from fastapi import status,HTTPException
from app.model.database import engine
from pytz import timezone
import pytz
import re
from random import randint
from io import BytesIO,StringIO
import base64
import csv
import ast
import re
import threading

tz = pytz.timezone("Asia/Kolkata")
def check_unique_rabbit_id(id_val:str):
    db_session=SessionLocal()
    
    id_count = db_session.query(models.TRabbitMessageTracker).filter(id==id_val).count()
    if id_count==0:
        db_session.close()
        return True
    else:
        db_session.close()
        return False

def create_update_rabbit_message_entry(message_id:str,message:str,publisher_time:str,listener_time:str,from_service:str,to_service:str):
    #logger.info("")

    db_session = SessionLocal()
    connectiion_status = engine.pool.status()
    #print(f"connection status inside rabbit_message_entry :{connectiion_status}")
    logger.info(f"DUMPING Message Id and from_service and to_service::-{message_id}::{from_service}::{to_service}")
    existing_entry=db_session.query(models.TRabbitMessageTracker).filter(models.TRabbitMessageTracker.message_id==message_id).count()
    if existing_entry==0:#implies it is a new entry
        
        if to_service:
            logger.info(f"LOOKS DB HANGUP-{to_service}")
        
        
        
        new_entry = models.TRabbitMessageTracker(
                    message_id=message_id,
                    publisher_message = json.dumps(message),
                    #publisher_time=datetime.datetime.strptime(publisher_time,"%Y-%m-%d %H:%M:%S"),
                    publisher_time=publisher_time,
                    from_service = from_service,
                    listener_time = listener_time,
                    to_service = to_service,
                    creation_date=datetime.datetime.now(pytz.timezone("Asia/Kolkata")),
                    last_update_time=datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                    )
        db_session.add(new_entry)
        db_session.commit()
       # db_session.close()
        logger.debug(f"Added Entry:{new_entry.__dict__}")
    elif existing_entry==1:
        update_entry=db_session.query(models.TRabbitMessageTracker).filter(models.TRabbitMessageTracker.message_id==message_id).one()
        
        if from_service:
            logger.info(f"DUMPING::from_service-{from_service}::{message_id}")
            update_entry.publisher_time = publisher_time,
            update_entry.from_service = from_service
            last_update_time=datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        elif to_service:
            logger.info(f"DUMPING::to_service-{to_service}::{message_id}")
            update_entry.listener_time = listener_time,
            update_entry.to_service = to_service
            last_update_time=datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    
        db_session.commit()
       # db_session.close()
        
    return True
lock_thread = threading.Lock()
def publish_message(message,db_session:DBSession):
    #lock_thread.acquire(1)
    print(f"Acquired lock for {message}")
    is_unique=False
    while not is_unique:
        id = uuid.uuid1().hex
        is_unique = check_unique_rabbit_id(id)
    
    #message = json.loads(message)
    

    connectiion_status = engine.pool.status()
    

    #print(f"connection status inside publish message is :{connectiion_status}")
    # crp_id = "crp_"+id
    # dbp_id = "dbp_"+id
    # message_for_chat_listener = {"crp_id":crp_id,"message":message}
    # message_for_db_listener = {"dbp_id":dbp_id,"message":message}
    # print(message_for_chat_listener)
    # print(message_for_db_listener)
    # time_publish = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
    # is_inserted = create_update_rabbit_message_entry(crp_id,message_for_chat_listener,time_publish,None,"publisher-chat-response",None)
    # logger.info("Insert Status:{}".format(is_inserted))
    # #crp=ChatResponsePublisher()
    # crp_thread = threading.Thread(target=ChatResponsePublisher.run, daemon=True)
    # crp_thread.start()
    # logger.info(f"Connection is {ChatResponsePublisher.publisher._connection}")
    # ChatResponsePublisher.publish(json.dumps(message_for_chat_listener))
    # logger.info(f'MESSAGE PUBLISHED  in Chat Queue:: {message_for_chat_listener}')
    # is_inserted = create_update_rabbit_message_entry(dbp_id,message_for_db_listener,time_publish,None,"publisher-db-insert",None)
    # #dbp = DBInsertPublisher()
    # dbp_thread = threading.Thread(target=DBInsertPublisher.run, daemon=True)
    # dbp_thread.start()
    # DBInsertPublisher.publish(json.dumps(message_for_db_listener))
    # logger.info(f'MESSAGE PUBLISHED  in DB Queue:: {message_for_db_listener}')

    crp_id = "crp_"+id
    dbp_id = "dbp_"+id
    message_for_chat_listener = {"crp_id":crp_id,"message":message}
    message_for_db_listener = {"dbp_id":dbp_id,"message":message}
    time_publish = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
    is_inserted = create_update_rabbit_message_entry(crp_id,message_for_chat_listener,time_publish,None,"publisher-chat-response",None)
    logger.info("Insert Status:{}".format(is_inserted))

    ChatResponsePublisher.publish(json.dumps(message_for_chat_listener))
    logger.info(f'MESSAGE PUBLISHED  in Chat Queue:: {message_for_chat_listener}')
    is_inserted = create_update_rabbit_message_entry(dbp_id,message_for_db_listener,time_publish,None,"publisher-db-insert",None)
    DBInsertPublisher.publish(json.dumps(message_for_db_listener))
    logger.info(f'MESSAGE PUBLISHED  in DB Queue:: {message_for_db_listener}')
    #lock_thread.release()
    return True

    

if __name__=="__main__":
    message = {"crp_id":"123","message":"message"}
    crp = ChatResponsePublisher()
    crp_thread = threading.Thread(target=crp.run)
    crp_thread.start()
    crp.publisher.publish(message)
    # db_session = SessionLocal()
    # print(db_session)
    # payload=json.dumps({"message":"hi"})
    # publish_message(payload,db_session)

