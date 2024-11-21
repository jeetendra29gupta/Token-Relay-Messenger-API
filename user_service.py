import logging
import os
from datetime import datetime
from typing import Optional

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import status, FastAPI, Header, HTTPException
from pydantic import BaseModel

from log_config import setup_logging

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8282/")
MESSAGE_SERVICE_URL = os.getenv("MESSAGE_SERVICE_URL", "http://localhost:8383/")

app = FastAPI()


# Pydantic models for user data
class LoginUser(BaseModel):
    username: str
    password: str


class SignupUser(LoginUser):
    email: str
    is_admin: bool


@app.post("/user/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def user_signup(user: SignupUser) -> dict:
    try:
        new_user = user.model_dump()

        auth_response = requests.post(f"{AUTH_SERVICE_URL}signup", json=new_user)
        auth_response.raise_for_status()

        logger.info(auth_response.json())

    except Exception as err:
        logger.error(err, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Auth service error: {err}")

    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": auth_response.json().get("detail"),
        "date_time": date_time,
    }


@app.post("/user/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login(user: LoginUser) -> dict:
    try:
        user_details = user.model_dump()

        auth_response = requests.post(f"{AUTH_SERVICE_URL}login", json=user_details)
        auth_response.raise_for_status()

        logger.info(auth_response.json())

    except Exception as err:
        logger.error(err, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Auth service error: {err}")

    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        "status_code": status.HTTP_200_OK,
        "detail": auth_response.json().get("token"),
        "date_time": date_time,
    }


@app.get("/user/message", response_model=dict, status_code=status.HTTP_200_OK)
async def user_message(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "Authorization token is missing",
            "date_time": date_time,
        }
    # Validate token with Auth Service
    try:
        auth_response = requests.post(f"{AUTH_SERVICE_URL}validate-token", headers={"token": authorization})
        auth_response.raise_for_status()
        is_valid = auth_response.json().get("is_valid", False)
        is_admin = auth_response.json().get("is_admin", False)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Auth service error: {e}")

    # Fetch message from Message Service
    try:
        message_response = requests.post(f"{MESSAGE_SERVICE_URL}get-message",
                                         json={"is_valid": is_valid, "is_admin": is_admin})
        message_response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Message service error: {e}")

    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        "status_code": status.HTTP_200_OK,
        "detail": message_response.json().get("message"),
        "date_time": date_time,
    }


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "User Service is up and running!"}


if __name__ == '__main__':
    uvicorn.run("user_service:app", host="0.0.0.0", port=8181, reload=True)
