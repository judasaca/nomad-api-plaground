from requests import request
from utils.logger import logger
from utils.api_client import APIClient
from tqdm import tqdm

from utils.zip_utils import zip_folder_in_memory


def download_upload_bundle(upload_id: str, client: APIClient):
    url = f"/uploads/{upload_id}/bundle"

    response = client.get(url, stream=True)
    response.raise_for_status()

    total_downloaded = 0
    chunk_size = 8192
    filename = f"./files/bundle/{upload_id}.zip"

    with (
        open(filename, "wb") as f,
        tqdm(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Downloading upload bundle",
        ) as progress,
    ):
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                size = len(chunk)
                f.write(chunk)
                total_downloaded += size
                progress.update(size)

    print(
        f"✅ Download complete. Total size: {total_downloaded / 1024 / 1024 / 1024:.2f} GB",
        f"Upload id: {upload_id}",
        sep="\n",
    )


def post_upload_bundle(upload_id: str, client: APIClient):
    url = "/uploads/bundle"
    with open(f"./files/bundle/{upload_id}.zip", "rb") as f:
        f.seek(0)

        class Stream:
            def __init__(self, file_obj):
                self.file = file_obj

            def __iter__(self):
                while chunk := self.file.read(8192):
                    yield chunk

        headers = {"Content-Type": "application/zip"}
        response = client.post(url, data=Stream(f), headers=headers)


def delete_upload(upload_id: str, client: APIClient):
    res = client.delete(f"/uploads/{upload_id}")


def publish_upload_to_main_deployment(upload_id: str, client: APIClient):
    res = client.post(
        f"/uploads/{upload_id}/action/publish", params={"to_central_nomad": True}
    )


def transfer_upload_with_bad_token(upload_id: str):
    local_client = APIClient(
        base_url="http://localhost:8000/fairdi/nomad/latest/api/v1"
    )
    oasis_client = APIClient(base_url="http://localhost:80/nomad-oasis/api/v1")
    oasis_token = oasis_client._token

    # Clean up target oasis upload
    delete_upload(upload_id, client=oasis_client)

    res = local_client.post(
        f"/uploads/{upload_id}/action/transfer",
        json={
            # "target_deployment_url": "http://localhost:80/nomad-oasis/api",
            "auth_token": "abcdefghtedas",
            "embargo_length": 5,
        },
    )


def transfer_upload(upload_id: str):
    local_client = APIClient(
        base_url="http://localhost:8000/fairdi/nomad/latest/api/v1"
    )
    oasis_client = APIClient(base_url="http://localhost:80/nomad-oasis/api/v1")
    oasis_token = oasis_client._token

    # Clean up target oasis upload
    delete_upload(upload_id, client=oasis_client)

    res = local_client.post(
        f"/uploads/{upload_id}/action/transfer",
        json={
            # "target_deployment_url": "http://localhost:80/nomad-oasis/api",
            "auth_token": oasis_token,
            "embargo_length": 5,
        },
    )


def get_upload(upload_id: str, client: APIClient):
    res = client.get(f"/uploads/{upload_id}")
    logger.debug(res.json())


def create_new_upload(client: APIClient):
    buffer = zip_folder_in_memory("./files/test_multi_delete")
    files = {"file": ("test_multi_delete.zip", buffer, "application/zip")}
    response = client.post("/uploads", files=files)


def delete_single_raw_file(upload_id: str, path: str, client: APIClient):
    response = client.delete(f"/uploads/{upload_id}/raw/{path}")
    return response
