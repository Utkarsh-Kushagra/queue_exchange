
from fastapi import APIRouter,Form
from message_exchange.publishers import crp as ChatResponsePublisher
import json

import logging
logger = logging.getLogger(__name__)



router=APIRouter()

@router.post('/send-message')
async def get_medicine_info(message:str = Form(...)):
    ChatResponsePublisher.publish(json.dumps({"data":message}))
    return f'Message Published : {message}'

