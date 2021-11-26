
from fastapi import APIRouter,Form,Request
from fastapi.param_functions import Depends
import requests
from sqlalchemy.orm import Session as DBSession
from app.database.queries import publish_message
from app.model.database import get_db
from app.model import schemas
from app.worker.worker import create_message
import json
import datetime
import pytz
import logging
logger = logging.getLogger(__name__)



router=APIRouter()



@router.post('/send-message')
async def send_message(message:str=Form(...),db: DBSession = Depends(get_db)):
    # insert in DB before publishing
    #print(message)
    #publish_result = publish_message(message,db)
    publish_result = create_message(message)
    
    
    return f'Message Published : {message}'



# @router.post('/send-message')
# async def send_message(message:str=Form(...)):
#     # insert in DB before publishing
#     #print(message)
#     #publish_result = create_message(message)
    
    
#     return f'Message Published : {message}'
