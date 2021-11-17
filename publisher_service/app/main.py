import os
import threading
import logging
from fastapi.middleware.cors import CORSMiddleware
logging.config.fileConfig("./app/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
from app.api.v1.routes import router


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
from app.message_exchange.publishers import crp as ChatResponsePublisher
from app.message_exchange.publishers import dbp as DBInsertPublisher

app = FastAPI(
	title="backend-services",
	description="REST API"
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count","Content-Range"]
    )

app.router.include_router(router, prefix="/publisher-service")
# initializing publisher
@app.on_event("startup")
def handle_startup():
    logger.info("*"*30)
    logger.info("Initializing conversation engine.")
    

    x = threading.Thread(target=ChatResponsePublisher.run, daemon=True)
    x.start()

    y = threading.Thread(target=DBInsertPublisher.run, daemon=True)
    y.start()

    # Add code above this line
    logger.info("Application startup event.")
    logger.info("*"*30)
