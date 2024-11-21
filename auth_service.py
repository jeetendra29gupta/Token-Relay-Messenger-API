import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Header, status, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from log_config import setup_logging
from models import User, init_db
from utils import hash_password, verify_password, create_token, get_current_user

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI()
init_db()


# Pydantic models for user data
class LoginUser(BaseModel):
    username: str
    password: str


class SignupUser(LoginUser):
    email: str
    is_admin: bool


@app.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user: SignupUser, db: Session = Depends(get_db)) -> dict:
    """Create a new user."""
    try:
        if db.query(User).filter(User.username == user.username).first():
            error_message = f"Username: {user.username}, already registered"
            logger.error(error_message, exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

            # Check if the email already exists
        if db.query(User).filter(User.email == user.email).first():
            error_message = f"Email ID: {user.email}, already registered"
            logger.error(error_message, exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, email=user.email, password=hashed_password, is_admin=user.is_admin)
        # Add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "detail": f"User created successfully, user ID {new_user.id}!",
            "user": {"email": new_user.email, "username": new_user.username},
            "date_time": date_time,
        }

    except Exception as err:
        logger.error(f"Error creating user: {err}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while creating the user.")


@app.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login(user: LoginUser, db: Session = Depends(get_db)) -> dict:
    """Authenticate a user and return tokens."""
    try:

        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user is None:
            error_message = "Invalid username"
            logger.error(error_message, exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

        # Verify the password
        if not verify_password(user.password, db_user.password):
            error_message = "Invalid password"
            logger.error(error_message, exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

        # Create tokens for the user
        tokens = create_token(db_user.username)
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "detail": "Login successful",
            "date_time": date_time,
            "token": tokens,
        }

    except Exception as err:
        logger.error(f"Error during login: {err}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login.")


@app.post("/validate-token", response_model=dict, status_code=status.HTTP_200_OK)
async def validate_token(token: str = Header(...), db: Session = Depends(get_db)) -> dict:
    try:

        if not token:
            raise HTTPException(status_code=400, detail="Token is missing")

        current_user = await get_current_user(token)
        db_user = db.query(User).filter(User.username == current_user).first()
        if db_user is None:
            error_message = "Invalid username"
            logger.error(error_message, exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "is_valid": True,
            "date_time": date_time,
            "user": current_user,
            "is_admin": db_user.is_admin,
        }

    except Exception as err:
        logger.error(f"Error during validate token: {err}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login.")


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Auth Service is up and running!"}


if __name__ == '__main__':
    uvicorn.run("auth_service:app", host="0.0.0.0", port=8282, reload=True)
