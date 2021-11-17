from pytz import timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time, Text
from sqlalchemy.orm import relationship
import datetime
import enum
from sqlalchemy.sql.sqltypes import SmallInteger
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql import JSON
from app.model.database import Base


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