from config import settings
import requests



def get_token(base_path: str, username: str, password: str):
    response = requests.post(
        base_path + "/auth/token",
        data={
            "username": username,
            "password": password,
        },
    )
    body = response.json()
    print(response)
    token = body['access_token']
    return token
