from pprint import pprint
from tqdm import tqdm

from actions.auth import check_health, get_user_info
from actions.uploads import delete_upload, download_upload_bundle, post_upload_bundle, publish_upload_to_main_deployment, transfer_upload
from utils.api_client import APIClient
from utils.auth import get_token
from utils.logger import configure_logger








def main():
    upload_id = "tmNTuQ_bSOGWTCBDIUjmcA"
    #print(get_token())
    #get_user_info()

    #delete_upload(upload_id)
    #post_upload_bundle(upload_id)
    #publish_upload_to_main_deployment(upload_id)

    #download_upload_bundle(upload_id)

    transfer_upload(upload_id)
    #check_health()

if __name__ == "__main__":
    main()
