import json

from utils.api_client import APIClient


def list_project_files(client: APIClient, project_id: str):
    response = client.post(
        "graph/query",
        json={
            "uploads": {
                project_id: {
                    "files": {
                        "m_request": {
                            "depth": 1,
                            "directive": "resolved",
                            "pagination": {"page": 1, "page_size": 20},
                        },
                    }
                }
            }
        },
    )

    return json.dumps(response.json()["uploads"][project_id]["files"], indent=2)
