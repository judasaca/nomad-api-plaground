from config import settings
import requests


_api_base_path = settings.api_base_path


def get_token():
    response = requests.post(
        _api_base_path + "/auth/token",
        data={
            "username": settings.username,
            "password": settings.password.get_secret_value(),
        },
    )
    body = response.json()
    token = f"Bearer {body['access_token']}"
    return token
