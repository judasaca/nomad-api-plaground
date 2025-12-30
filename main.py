from actions.uploads import (
    download_upload_bundle,
)
from utils.api_client import APIClient


def main():
    upload_id = "0vEOe4LRQ0iUa69J9591nA"
    local_client = APIClient()
    download_upload_bundle(upload_id, local_client)


if __name__ == "__main__":
    main()
