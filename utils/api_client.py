from pprint import pformat, pprint
from typing import Any, Dict, Optional, Union
import requests
from urllib.parse import urljoin

from config import settings
from loguru import logger
from utils.auth import get_token


class APIClient:
    def __init__(self, authenticated: bool = True):
        self.base_url = settings.api_base_path
        self.session = requests.Session()
        if authenticated:
            self._token = get_token()
            self.session.headers.update({"Authorization": self._token})
        else:
            self._token = None
        logger.info("Client started. Base url: {}", self.base_url)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> requests.Response:
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        logger.info(f"Hitting... {path}")
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=files,
            timeout=timeout,
            **kwargs,
        )
        content_type = response.headers["content-type"]
        if content_type == "application/json":
            response_time_ms = response.elapsed.total_seconds() * 1000
            # Determine color
            if response.ok:
                status_str = f"\033[92m{response.status_code}\033[0m"  # Green
            else:
                status_str = f"\033[91m{response.status_code}\033[0m"  # Red
            logger.info(
                """Response time: {response_time} ms\nStatus Code: {status_code} \nResponse JSON:\n\t{body}""",
                response_time=response_time_ms,
                body=pformat(response.json()),
                status_code=status_str
            )
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._request("PATCH", path, **kwargs)
