from actions.uploads import delete_upload, post_upload_bundle
from utils.api_client import APIClient


def reset_mutidelete_upload(upload_id: str, client: APIClient):
    delete_upload(upload_id, client)
    post_upload_bundle(upload_id, client)

