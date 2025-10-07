from pprint import pprint
from tqdm import tqdm

from actions.auth import check_health, get_user_info
from actions.uploads import (
    create_new_upload,
    delete_single_raw_file,
    delete_upload,
    download_upload_bundle,
    get_upload,
    post_upload_bundle,
    publish_upload_to_main_deployment,
    transfer_upload,
    transfer_upload_with_bad_token,
)
from utils.api_client import APIClient
from utils.auth import get_token
from utils.logger import configure_logger
from utils.multi_delete_utils import reset_mutidelete_upload


def main():
    upload_id = "tmNTuQ_bSOGWTCBDIUjmcA"
    # print(get_token())
    # get_user_info()

    local_client = APIClient()
    # create_new_upload(local_client)
    # post_upload_bundle(upload_id, client=local_client)
    # publish_upload_to_main_deployment(upload_id)

    test_for_multidelete_bundle_id = "5UbdsQ4hQvih1TBQi1a_vQ"
    # download_upload_bundle(test_for_multidelete_bundle_id, local_client)
    reset_mutidelete_upload(test_for_multidelete_bundle_id, local_client)
    delete_single_raw_file(upload_id, "a_0/a_00.txt", local_client)

    # transfer_upload_with_bad_token(upload_id)
    # oasis_client = APIClient(base_url="http://localhost/nomad-oasis/api/v1")
    # print(oasis_client._token)
    # delete_upload(upload_id, oasis_client)
    # check_health()
    # get_upload(upload_id, local_client)


if __name__ == "__main__":
    main()
