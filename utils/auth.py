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
    token = body['access_token']
    return token
