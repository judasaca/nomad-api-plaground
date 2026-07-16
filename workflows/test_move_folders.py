from actions.uploads import create_new_upload, get_uploads_by_name
from utils.api_client import APIClient


def test_move_folders(client: APIClient):
    upload_name = "test_move_folders"
    uploads = get_uploads_by_name(upload_name, client).json()["data"]
    print(f"Uploads found: {len(uploads)}")
    for upload in uploads:
        upload_id = upload["upload_id"]
        client.delete(f"/uploads/{upload_id}")

    create_response = create_new_upload(
        client, name=upload_name, source_folder="./nested_tree"
    )
    upload_id = get_uploads_by_name(upload_name, client).json()["data"]
    print(uploads[0]["upload_id"])
    # Move folders
    try:
        target_folder = ""
        sourceFolder = ""
        folderName = ""
        move_response = client.post(
            f"/uploads/{upload_id}/raw/{target_folder}",
            params={
                "copy_or_move": "move",
                "copy_or_move_source_path": sourceFolder,
                "file_name": folderName,
            },
        )

        assert move_response.status_code == 200
        print(f"Move folders response: {move_response.text}")
    finally:
        uploads = get_uploads_by_name(upload_name, client).json()["data"]


if __name__ == "__main__":
    local_client = APIClient()
    test_move_folders(local_client)
