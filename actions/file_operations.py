from utils.api_client import APIClient


def rename_file(client: APIClient, upload_id: str, file_path: str, new_file_name: str):
    folder_path = "/".join(file_path.split("/")[:-1]) if "/" in file_path else ""
    res = client.put(
        f"/uploads/{upload_id}/raw/{folder_path}",
        params={
            "copy_or_move": "move",
            "file_name": new_file_name,
            "copy_or_move_source_path": file_path,
        },
    )
    print(res.url)

