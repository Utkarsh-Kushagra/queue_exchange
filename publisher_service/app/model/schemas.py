from datetime import date, datetime
from app.model.database import Base
from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, Request, Body

class publishRequest(BaseModel):
    message:str
    