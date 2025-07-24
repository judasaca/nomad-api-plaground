from pprint import pprint
from tqdm import tqdm

from utils.api_client import APIClient




def get_user_info():
    response = client.get("/users/me")
    user_info = response.json()
    pprint(user_info)




def main():
    upload_id = "tmNTuQ_bSOGWTCBDIUjmcA"
    #download_upload_bundle(upload_id)
    post_upload_bundle(upload_id)
    #delete_upload(upload_id)


if __name__ == "__main__":
    main()
