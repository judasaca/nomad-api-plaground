from pprint import pprint

import requests
from utils.api_client import APIClient


client = APIClient()
def get_user_info():
    response = client.get("/users/me")
    user_info = response.json()
    pprint(user_info)

def check_health():
    response = requests.get("http://localhost:8000/-/health")
    print(response)
