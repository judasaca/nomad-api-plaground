import json
from pprint import pformat
from loguru import logger
from config import settings
import requests



def get_token(base_path: str, username: str, password: str):
    print(base_path, username, password)
    response = requests.post(
        base_path + "/auth/token",
        data={
            "username": username,
            "password": password,
        },
    )
    body = response.json()
    if response.status_code != 200:
        logger.error('failed to auth user')
        logger.error(pformat(body))
        raise Exception('Auth failed')
    token = body['access_token']
    return token
