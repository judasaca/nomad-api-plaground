from json import dumps
from pprint import pformat, pprint
from rich.syntax import Syntax
from typing import Any, Dict, Optional, Union
import requests
from urllib.parse import urljoin

from config import settings
from loguru import logger
from utils.auth import get_token
from utils.logger import log_timing
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.panel import Panel


console = Console()


class APIClient:
    def __init__(self, authenticated: bool = True, base_url: str | None = None):
        self.base_url = base_url or settings.api_base_path
        self.session = requests.Session()
        if authenticated:
            self._token = get_token(
                base_path=self.base_url,
                username=settings.username,
                password=settings.password.get_secret_value(),
            )
            self.session.headers.update({"Authorization": f"Bearer {self._token}"})
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
        print_body: bool = False,
        **kwargs,
    ) -> requests.Response:
        header_text = Text()
        header_text.append(f"Base: {self.base_url}")
        header_text.append(f"{method} ", style="bold cyan")
        header_text.append(f"{path}\n", style="bold white")
        header_text.append("Status: ", style="bold")
        header_text.append("pending...", style="yellow")
        header_text.append("\nTime: ", style="bold")
        header_text.append("—", style="dim")

        url = urljoin(self.base_url + "/", path.lstrip("/"))
        panel = Panel(header_text, border_style="dim", title="Request", expand=False)
        with Live(panel, refresh_per_second=8, console=console):
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
            status = response.status_code
            if 200 <= status < 300:
                status_color = "green"
            elif 300 <= status < 400:
                status_color = "yellow"
            else:
                status_color = "red"

            # --- build updated info ---
            header_text = Text()
            header_text.append(f"{method} ", style="bold cyan")
            header_text.append(f"{url}\n", style="bold white")
            header_text.append("Status: ", style="bold")
            header_text.append(f"{status}\n", style=status_color)
            header_text.append("Time: ", style="bold")
            header_text.append(
                f"{response.elapsed.total_seconds() * 1000:.1f} ms\n", style="blue"
            )
            content_type = response.headers["content-type"]
            if content_type == "application/json":
                body_json = response.json()
                syntax = Syntax(
                    dumps(body_json, indent=2),
                    "json",
                    theme="monokai",
                    line_numbers=False,
                )
                body_renderable = syntax

            # update the live panel
            console.print(Panel(header_text, title="Response", border_style=status_color, expand=False))
            console.print(panel)
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
