import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8181/")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8282/")
MESSAGE_SERVICE_URL = os.getenv("MESSAGE_SERVICE_URL", "http://localhost:8383/")

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_session():
    """Create a requests session with default headers."""
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    session.headers.update({'Accept': 'application/json'})
    return session


def user_signup(session, base_url, user):
    try:
        uri = f"{base_url}user/signup"
        logging.info(f"Making request to {uri} with user details: {user}")
        response = session.post(uri, json=user)
        response.raise_for_status()
        logging.info(f"Response: {response.json()}")

    except Exception as err:
        logging.error(f"Error: {err}")
        raise


def user_login(session, base_url, user):
    try:
        uri = f"{base_url}user/login"
        logging.info(f"Making request to {uri} with user details: {user}")
        response = session.post(uri, json=user)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Response: {data}")
        return data
    except Exception as err:
        logging.error(f"Error: {err}")
        raise


def get_user_message(session, base_url, token):
    try:
        uri = f"{base_url}user/message"
        logging.info(f"Making request to {uri} with token: {token}")
        response = session.get(uri, headers={'Authorization': token})
        response.raise_for_status()
        logging.info(f"Response: {response.json()}")
    except Exception as err:
        logging.error(f"Error: {err}")
        raise


if __name__ == '__main__':
    try:
        request_session = get_session()

        # admin_signup_user = {
        #     "username": "admin_user", "password": "admin_user_password",
        #     "email": "admin_user@email.com", "is_admin": "true",
        # }
        # user_signup(request_session, USER_SERVICE_URL, admin_signup_user)
        #
        # normal_signup_user = {
        #     "username": "normal_user", "password": "normal_user_password",
        #     "email": "normal_user@email.com", "is_admin": "false"
        # }
        # user_signup(request_session, USER_SERVICE_URL, normal_signup_user)

        admin_login_user = {"username": "admin_user", "password": "admin_user_password", }
        output = user_login(request_session, USER_SERVICE_URL, admin_login_user)
        access_token = output.get("detail").get("access_token")
        get_user_message(request_session, USER_SERVICE_URL, access_token)

        normal_login_user = {"username": "normal_user", "password": "normal_user_password", }
        output = user_login(request_session, USER_SERVICE_URL, normal_login_user)
        access_token = output.get("detail").get("access_token")
        get_user_message(request_session, USER_SERVICE_URL, access_token)


    except Exception as ex:
        logging.error(f"An error occurred: {ex}", exc_info=True)
