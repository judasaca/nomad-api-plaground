from pprint import pprint

import requests
from utils.api_client import APIClient


def get_user_info(client: APIClient):
    response = client.get("/users/me")
    user_info = response.json()

def check_health():
    response = requests.get("http://localhost:8000/-/health")
    print(response)
