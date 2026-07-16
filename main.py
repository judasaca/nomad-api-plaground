from actions.uploads import (
    download_upload_bundle,
)
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
    local_client = APIClient()
    # slow_operations = 0
    # test_iterations = 20
    # for i in range(test_iterations):
    #    # print("-" * 40)
    #    print(f"Running iteration {i + 1}")
    #    total_time = create_upload_upload_file_and_delete(local_client)
    #    if total_time > 7:
    #        print("found!")
    #        slow_operations += 1
    # print("-" * 40)
    # print(f"Total slow operations: {slow_operations} out of {test_iterations}")
    # test_create_first_and_then_delete(local_client)
    entry_id = "ugNqctzstxK6JfzeLQuPMaEn4b0w"
    response = local_client.post(
        "/graph/query",
        json={
            "entries": {
                entry_id: {
                    "archive": {
                        "m_def": {"m_request": {"directive": "plain"}},
                        "m_request": {
                            "depth": 1,
                            "directive": "plain",
                            "m_def_format": "short",
                        },
                        "run[0]": {
                            "m_def": {"m_request": {"directive": "plain"}},
                            "m_request": {
                                "depth": 1,
                                "directive": "plain",
                                "include_definition": "both",
                                "m_def_format": "short",
                                # "max_list_size": 3,
                            },
                            "calculation": {
                                "m_request": {
                                    "depth": 1,
                                    "pagination": {"page": 1, "page_size": 5},
                                    # "index": [0, 5],
                                    "directive": "plain",
                                },
                            },
                        },
                    }
                }
            }
        },
    )

    # entries_response = local_client.post(
    #    f"/entries/{entry_id}/archive/query",
    #    json={
    #        "pagination": {"page": 1, "page_size": 5},
    #        "required": {"run[0]": {"*": {"pagination": {"page": 1, "page_size": 5}}}},
    #        "query": {"*": {"pagination": {"page": 1, "page_size": 5}}},
    #    },
    # )
    try:
        body_json = response.json()
        calculations = body_json["entries"][entry_id]["archive"]["run"][0][
            "calculation"
        ]

        print(calculations)
        # entries_response_json = entries_response.json()
        # pprint(entries_response_json)
    except Exception:
        pass
        print(response.json())


if __name__ == "__main__":
    main()
