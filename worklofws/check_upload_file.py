from time import sleep, time

from tqdm import tqdm

from actions.uploads import create_new_upload, delete_single_raw_file, delete_upload
from graph.graph import list_project_files
from utils.api_client import APIClient


def upload_sample_file(file_name: str, client: APIClient):
    upload_id = "EODzdTAeR4WhbNZr6l5Xkg"
    file_content = "This is a sample file for testing."
    files = {"file": (file_name, file_content, "text/plain")}
    response = client.put(f"/uploads/{upload_id}/raw/", files=files)
    if response.status_code == 200:
        print(f"File '{file_name}' uploaded successfully")
    else:
        print(f"Failed to upload file '{file_name}': {response.text}")


def check_upload_file(client: APIClient):
    upload_id = "EODzdTAeR4WhbNZr6l5Xkg"
    file_name = "file1.txt"
    # delete_single_raw_file(upload_id, file_name, client)
    upload_sample_file(file_name, client)
    print("Fetching files")
    files = list_project_files(client, upload_id)
    file_found = file_name in files
    while not file_found:
        waiting_time = 5
        print(
            f"File '{file_name}' not found, waiting {waiting_time} seconds and retrying..."
        )
        sleep(waiting_time)  # Wait for 2 seconds before retrying
        print("Fetching files")
        files = list_project_files(client, upload_id)
        file_found = file_name in files
    print(f"File '{file_name}' found")
    delete_single_raw_file(upload_id, file_name, client)


def create_upload_upload_file_and_delete(client: APIClient) -> float:
    upload_name = "concurrent test"
    create_response = create_new_upload(client, name=upload_name)
    # print("Created upload", create_response.status_code)
    uploads = client.get("/uploads", params={"upload_name": upload_name}).json()["data"]

    for upload in uploads:
        upload_id = upload["upload_id"]
        while True:
            initial_time = time()
            response = delete_upload(upload_id, client=client)
            if response.status_code == 200:
                total_time = time() - initial_time
                # if (total_time > 3):
                #    print(f"Slow delete operation for upload {upload_id}. Took {total_time:.2f} seconds.")
                print(
                    f"Delete operation took {total_time:.2f} seconds. Status code: {response.status_code}\n"
                )
                return total_time

            else:
                # print(f"Failed to delete upload {upload_id}. Status code: {response.status_code}. Retrying...")
                sleep(1)  # Wait for 1 second before retrying
        # print("Deleted upload", response.status_code)


def test_create_first_and_then_delete(client: APIClient):
    upload_names = [f"concurrent test {i}" for i in range(10)]
    create_times = []
    delete_times = []
    waiting_time_threshold = 7  # seconds
    for _ in tqdm(range(7)):
        for upload_name in upload_names:
            create_start = time()
            create_new_upload(client, name=upload_name)
            create_time = time() - create_start
            create_times.append(create_time)

        for upload_name in upload_names:
            uploads = client.get(
                "/uploads", params={"upload_name": upload_name}
            ).json()["data"]
            for upload in uploads:
                upload_id = upload["upload_id"]
                delete_start = time()
                delete_upload(upload_id, client=client)
                delete_time = time() - delete_start
                delete_times.append(delete_time)

    print("Create times statistics:")
    print(f"Average create time: {sum(create_times) / len(create_times):.2f} seconds")
    print(f"Max create time: {max(create_times):.2f} seconds")
    print(f"Min create time: {min(create_times):.2f} seconds")
    print(
        f"percentage of create operations above threshold:  {sum(1 for t in create_times if t > waiting_time_threshold) / len(create_times) * 100:.2f}%"
    )
    print("_" * 40, "\n")
    print("Delete times statistics:")
    print(f"Average delete time: {sum(delete_times) / len(delete_times):.2f} seconds")
    print(f"Max delete time: {max(delete_times):.2f} seconds")
    print(f"Min delete time: {min(delete_times):.2f} seconds")
    print(
        f"percentage of delete operations above threshold:  {sum(1 for t in delete_times if t > waiting_time_threshold) / len(delete_times) * 100:.2f}%"
    )
    print("_" * 40)
