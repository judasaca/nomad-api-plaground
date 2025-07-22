from config import settings
import requests
from pprint import pprint
from tqdm import tqdm

api_base_path = settings.api_base_path


def get_token():
    response = requests.post(
        api_base_path + "/auth/token",
        data={
            "username": settings.username,
            "password": settings.password.get_secret_value(),
        },
    )
    body = response.json()
    token = f"Bearer {body['access_token']}"
    return token


def get_user_info():
    token = get_token()
    response = requests.get(
        api_base_path + "/users/me", headers={"Authorization": token}
    )
    user_info = response.json()
    pprint(user_info)



def download_upload_bundle(upload_id: str):
    token = get_token()
    url = api_base_path + f"/uploads/{upload_id}/bundle"

    response = requests.get(url, headers={"Authorization": token}, stream=True)
    response.raise_for_status()

    total_downloaded = 0
    chunk_size = 8192
    filename = f"./files/bundle/{upload_id}.zip"

    with open(filename, "wb") as f, tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc="Downloading",
    ) as progress:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                size = len(chunk)
                f.write(chunk)
                total_downloaded += size
                progress.update(size)

    print(f"✅ Download complete. Total size: {total_downloaded / 1024 / 1024 / 1024:.2f} GB")


def main():
    download_upload_bundle(upload_id="tmNTuQ_bSOGWTCBDIUjmcA")


if __name__ == "__main__":
    main()
