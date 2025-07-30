from utils.api_client import APIClient
from tqdm import tqdm



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
        file_size = f.seek(0, 2)
        f.seek(0)
        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Posting upload bundle"
        ) as pbar:

            class Stream:
                def __init__(self, file_obj):
                    self.file = file_obj

                def __iter__(self):
                    while chunk := self.file.read(8192):
                        pbar.update(len(chunk))
                        yield chunk

            headers = {"Content-Type": "application/zip"}
            response = client.post(url, data=Stream(f), headers=headers)


def delete_upload(upload_id: str, client: APIClient):
    res = client.delete(f"/uploads/{upload_id}")


def publish_upload_to_main_deployment(upload_id: str, client: APIClient):
    res = client.post(
        f"/uploads/{upload_id}/action/publish", params={"to_central_nomad": True}
    )


def transfer_upload(upload_id: str):
    local_client = APIClient(
        base_url="http://localhost:8000/fairdi/nomad/latest/api/v1"
    )
    oasis_client = APIClient(base_url="http://localhost:80/nomad-oasis/api/v1")
    oasis_token = oasis_client._token

    #Clean up target oasis upload
    delete_upload(upload_id, client=oasis_client)

    res = local_client.post(
        f"/uploads/{upload_id}/action/transfer",
        json={
            "target_deployment_url": "http://localhost:80/nomad-oasis/api",
            "auth_token": oasis_token,
        },
    )
