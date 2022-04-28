"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import json


class Request:
    """Class to handle Websocket Request Object."""

    def __init__(self) -> None:
        """Initialize Request object."""
        self.data = {"requests": [{"function": "", "params": []}]}

    def build_request(self, command: str, params: list) -> Request:
        """Build request with given parameter."""
        self.data["requests"][0]["function"] = command
        self.data["requests"][0]["params"] = params

        return self

    def get_data(self) -> dict:
        """Return Python dict with current data."""
        return self.data

    def get_json(self) -> str:
        """Return data converted into JSON String."""
        return json.dumps(self.data)
