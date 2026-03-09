from pprint import pprint

from utils.api_client import APIClient


def show_entries_metadata(client: APIClient, entry_id: str):
    path = f"/entries/{entry_id}"
    response = client.get(path)
    pprint(response.json())


def show_entry_metainfo(client: APIClient, entry_id: str, metainfo_section: str):
    path = "graph/query"
    body = {
        "entries": {
            entry_id: {
                "archive": {
                    "m_request": {
                        "directive": "plain",
                        "include_definition": "both",
                        "exclude": ["*"],
                    },
                    "m_def": {"m_request": {"directive": "plain"}},
                    "data": {
                        "m_request": {
                            "directive": "plain",
                            "include_definition": "both",
                            "depth": 1,
                        },
                        "m_def": {"m_request": {"directive": "plain"}},
                    },
                }
            }
        }
    }
    response = client.post(path, json=body).json()

    pprint(response["metainfo"][metainfo_section])
