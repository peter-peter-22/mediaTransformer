from fastapi import HTTPException
from src.common.env import settings
from fastapi import Header, HTTPException

def verify_secret_key(secret_key: str = Header(...)):
    if secret_key != settings.secret_key:
        raise HTTPException(401, "Invalid secret key.")