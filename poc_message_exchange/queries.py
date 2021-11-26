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


from sqlalchemy import desc, func,distinct
import datetime
from datetime import date, timedelta
import os

# from app.message_exchange.publishers import crp as ChatResponsePublisher
# from app.message_exchange.publishers import dbp as DBInsertPublisher

#from app.worker import worker
import pprint

import shutil
from os import name, path
from sqlalchemy import func

from fastapi.responses import FileResponse
from fastapi import status,HTTPException

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

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from pytz import timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time, Text
from sqlalchemy.orm import relationship
import datetime
import enum
from sqlalchemy.sql.sqltypes import SmallInteger
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql import JSON



SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysql123@localhost:33060/test_rabbit"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TRabbitMessageTracker(Base):
    __tablename__="t_rabbitmq_message_tracker"
    message_id=Column(String(32),primary_key=True)
    publisher_message=Column(Text())
    publisher_time=Column(DateTime)
    listener_time=Column(DateTime)
    from_service=Column(String(15))
    to_service=Column(String(15)) 
    creation_date=Column(DateTime,default=datetime.datetime.utcnow)
    last_update_time=Column(DateTime,default=datetime.datetime.utcnow)
# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


tz = pytz.timezone("Asia/Kolkata")
def check_unique_rabbit_id(id_val:str):
    db_session=SessionLocal()
    
    id_count = db_session.query(TRabbitMessageTracker).filter(id==id_val).count()
    if id_count==0:
        db_session.close()
        return True
    else:
        db_session.close()
        return False

def create_update_rabbit_message_entry(message_id:str,message:str,publisher_time:str,listener_time:str,from_service:str,to_service:str):
    #logger.info("")
    print(f"message id is {message_id}")
    db_session = SessionLocal()
    
    #print(f"connection status inside rabbit_message_entry :{connectiion_status}")
    print(f"DUMPING Message Id and from_service and to_service::-{message_id}::{from_service}::{to_service}")
    existing_entry=db_session.query(TRabbitMessageTracker).filter(TRabbitMessageTracker.message_id==message_id).count()
    if existing_entry==0:#implies it is a new entry
        
        if to_service:
            logger.info(f"LOOKS DB HANGUP-{to_service}")
        
        
        
        new_entry = TRabbitMessageTracker(
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
        update_entry=db_session.query(TRabbitMessageTracker).filter(TRabbitMessageTracker.message_id==message_id).one()
        
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


def insert_in_db(id,message,from_service):
    # is_unique=False
    # while not is_unique:
    #     id = uuid.uuid1().hex
    #     is_unique = check_unique_rabbit_id(id)
    time_publish = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
    is_inserted = create_update_rabbit_message_entry(id,message,time_publish,None,from_service,None)


def publish_message(message,db_session:DBSession):
    #lock_thread.acquire(1)
    print(f"Acquired lock for {message}")
    is_unique=False
    while not is_unique:
        id = uuid.uuid1().hex
        is_unique = check_unique_rabbit_id(id)
    
    
    #message = json.loads(message)
    

    connectiion_status = engine.pool.status()
    
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

import ast
def insert_acknowledgement(msg:str,to_service)->bool:
    msg = str(msg.decode('utf-8'))
    #print(type(json.loads(msg)))         
    #print(type(msg.decode('utf-8')))
    print(msg)
    #msg = json.dumps(msg)
    
    
    msg = ast.literal_eval(msg)
    
    tz = pytz.timezone("Asia/Kolkata")
    message_id = msg["message_id"]
    print(message_id)
    time_listen = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
    to_service = to_service
    time_publish = None
    from_service =None
    logger.info(f"Params for insert update:Rabbit:{message_id},{time_publish},{time_listen},{from_service},{to_service},{msg}")
    
    try:
        insert_update_response = create_update_rabbit_message_entry(message_id,msg,time_publish,time_listen,from_service,to_service)
    except Exception as e:
        logger.error(e)
        logger.error("Error Occured Here")
    #logger.info("Insert Result:{}".format(insert_update_response))
    return insert_update_response 

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

