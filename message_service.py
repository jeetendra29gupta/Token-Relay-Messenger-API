import logging

import uvicorn
from fastapi import FastAPI, Request, HTTPException, status

from log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

# Example of a message storage for demo purposes (can be replaced with a real database)
messages = {
    "admin": "Welcome, Admin! You have full access.",
    "user": "Welcome, Authenticated user! Limited access.",
    "guest": "Access denied. Invalid user."
}


@app.post("/get-message", response_model=dict, status_code=status.HTTP_200_OK)
async def get_message(request: Request) -> dict:
    """
    Get a message based on user validation and role.
    - is_valid: Indicates whether the user is valid.
    - is_admin: Indicates if the user is an admin.
    """
    try:
        # Extract the request body
        body = await request.json()

        is_valid = body.get("is_valid")
        if is_valid is None:
            raise HTTPException(status_code=400, detail="Missing 'is_valid' field")

        is_admin = body.get("is_admin")
        if is_admin is None:
            raise HTTPException(status_code=400, detail="Missing 'is_admin' field")

        if is_valid:
            if is_admin:
                return {"message": messages["admin"]}
            else:
                return {"message": messages["user"]}
        else:
            return {"message": messages["guest"]}

    except Exception as err:
        logger.error(f"Error processing message: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {err}")


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Message Service is up and running!"}


if __name__ == '__main__':
    uvicorn.run("message_service:app", host="0.0.0.0", port=8383, reload=True)
