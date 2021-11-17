import os
import threading
import logging
logging.config.fileConfig("./app/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


TRACE_LEVEL_NUM = 9 
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(TRACE_LEVEL_NUM, message, args, **kws) 
logging.Logger.trace = trace

PROFILE_LEVEL_NUM = 51
logging.addLevelName(PROFILE_LEVEL_NUM, "PROFILE")
def profile(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(PROFILE_LEVEL_NUM, message, args, **kws) 
logging.Logger.profile = profile

from fastapi import FastAPI
from app.message_exchange.listeners import dil as DBInsertListener
app = FastAPI()

@app.on_event("startup")
def handle_startup():
    logger.info("*"*30)
    logger.info("Initializing conversation engine.")
    logger.info("Starting chatty request/response listener and publisher.")
    DBInsertListener.run()


    # Add code above this line
    logger.info("Application startup event.")
    logger.info("*"*30)