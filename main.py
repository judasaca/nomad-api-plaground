from pprint import pprint
from tqdm import tqdm

from utils.api_client import APIClient


client = APIClient()


def get_user_info():
    response = client.get("/users/me")
    user_info = response.json()
    pprint(user_info)


def download_upload_bundle(upload_id: str):
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


def post_upload_bundle(upload_id: str):
    url = "/uploads/bundle"
    response = client.post(
        url,
    )
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
            print(response.status_code, response.text)


def delete_upload(upload_id: str):
    res = client.delete(f'/uploads/{upload_id}')


def main():
    upload_id = "tmNTuQ_bSOGWTCBDIUjmcA"
    #download_upload_bundle(upload_id)
    #post_upload_bundle(upload_id)
    delete_upload(upload_id)


if __name__ == "__main__":
    main()
