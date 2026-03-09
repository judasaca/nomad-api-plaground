from actions.uploads import (
    download_upload_bundle,
)
from entries.metadata import show_entry_metainfo
from utils.api_client import APIClient


def download_bundle_with_references():
    upload_id = "0vEOe4LRQ0iUa69J9591nA"  # This is the upload id that has a files referencing each other
    local_client = APIClient()
    download_upload_bundle(upload_id, local_client)


def start_action(client: APIClient):
    # action_id = quote("dummy_nomad_plugin.actions.myaction:my_action", safe="")
    action_id = "dummy_nomad_plugin.actions.myaction:my_action"
    path = f"/actions/{action_id}/start"
    response = client.post(path, json={"data": {"iterations": 5}})


def main():
    # upload_id = "0vEOe4LRQ0iUa69J9591nA"  # This is the upload id that has a files referencing each other
    local_client = APIClient()
    # response = local_client.get("/actions/schemas")
    # print(json.dumps(response.json(), indent=2))
    # start_action(local_client)
    entry_id = "vqMfh4k4AmdW18T75tUDZFnT5nRk"
    metainfo_section = "dummy_nomad_plugin.schema_packages.schema_package"
    show_entry_metainfo(local_client, entry_id, metainfo_section)
    metainfo_id = "46e0f876b712aded080ab12ac4e9f4c2b205f03a"
    # show_metainfo_of_section(local_client, metainfo_id)


if __name__ == "__main__":
    main()
