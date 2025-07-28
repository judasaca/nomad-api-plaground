from pprint import pprint
from utils.api_client import APIClient


client = APIClient()
def get_user_info():
    response = client.get("/users/me")
    user_info = response.json()
    pprint(user_info)
