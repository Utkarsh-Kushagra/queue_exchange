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

tz = pytz.timezone("Asia/Kolkata")
def check_unique_rabbit_id(id_val:str,db_session:DBSession):
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
    logger.debug(f"DUMPING Message Id and from_service and to_service::-{message_id}::{from_service}::{to_service}")
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
        db_session.close()
        
    return True

# def publish_message(message):
#     is_unique=False
#     while not is_unique:
#         id = uuid.uuid1().hex
#         is_unique = check_unique_rabbit_id(id)
#     crp_id = "crp_"+id
#     dbp_id = "dbp_"+id
#     time_publish = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
#     is_inserted = create_update_rabbit_message_entry(crp_id,message,time_publish,None,"publisher-chat-response",None)
#     logger.info("Insert Status:{}".format(is_inserted))

#     ChatResponsePublisher.publish(json.dumps({"data":message}))
#     logger.info(f'MESSAGE PUBLISHED  in Chat Queue:: {message}')
#     is_inserted = create_update_rabbit_message_entry(dbp_id,message,time_publish,None,"publisher-db-insert",None)
#     DBInsertPublisher.publish(json.dumps({"data":message}))
#     logger.info(f'MESSAGE PUBLISHED  in DB Queue:: {message}')


def insert_acknowledgement(msg:json)->bool:
          
    tz = pytz.timezone("Asia/Kolkata")
    message_id = msg["crp_id"]
    time_listen = datetime.datetime.strftime(datetime.datetime.now(tz).astimezone(tz).replace(tzinfo=None),"%Y-%m-%d %H:%M:%S.%f")
    to_service = "chat-listener"
    time_publish = None
    from_service =None
    logger.info(f"Params for insert update:Rabbit:{message_id},{time_publish},{time_listen},{from_service},{to_service},{json.dumps(msg)}")
    payload={
    "message_id":message_id,
    "message":json.dumps(msg),
    "publisher_time":time_publish,
    "listener_time":time_listen,
    "from_service":from_service,
    "to_service":to_service
    }
    logger.info(f"PAYLOAD:{payload}")
    try:
        insert_update_response = create_update_rabbit_message_entry(message_id,msg,time_publish,time_listen,from_service,to_service)
    except Exception as e:
        logger.error(e)
        logger.error("Error Occured Here")
    logger.info("Insert Result:{}".format(insert_update_response))
    return insert_update_response