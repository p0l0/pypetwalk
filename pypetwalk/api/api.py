"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import logging
from types import TracebackType

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from pypetwalk.const import (
    API_HTTP_PROTOCOL,
    API_PATH_MAPPING,
    API_STATE_DOOR,
    API_STATE_MAPPING_DOOR_CLOSE,
    API_STATE_MAPPING_DOOR_OPEN,
    API_STATE_MAPPING_SYSTEM_OFF,
    API_STATE_MAPPING_SYSTEM_ON,
    API_STATE_SYSTEM,
)
from pypetwalk.exceptions import (
    PyPetWALKClientConnectionError,
    PyPetWALKInvalidResponseStatus,
)

_LOGGER = logging.getLogger(__name__)


class API:
    """Class for handling local API calls."""

    def __init__(self, host: str, port: int) -> None:
        """Initialize API class."""
        self.server_host = host
        self.server_port = port
        self.session = ClientSession()

    async def __aenter__(self) -> "API":
        """Start API class from context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop API class from context manager."""
        await self.close()

    async def close(self) -> None:
        """Wait until all sessions are closed."""
        if self.session:
            await self.session.close()

    async def get_modes(self) -> dict:
        """Get current 'modes' from API."""
        return await self.send_command("mode", None)

    async def set_mode(self, mode: str, value: bool) -> dict:
        """Set new value for given 'mode'."""
        return await self.send_command("mode", {mode: value})

    async def get_states(self) -> dict:
        """Get current 'states' from API."""
        return await self.send_command("state", None)

    async def set_state(self, state: str, value: bool) -> dict:
        """Set new value for given 'state'."""
        if state == API_STATE_SYSTEM:
            new_state = API_STATE_MAPPING_SYSTEM_ON
            if not value:
                new_state = API_STATE_MAPPING_SYSTEM_OFF
        elif state == API_STATE_DOOR:
            new_state = API_STATE_MAPPING_DOOR_CLOSE
            if value:
                new_state = API_STATE_MAPPING_DOOR_OPEN
        return await self.send_command("state", {state: new_state})

    async def send_command(self, command: str, params: dict | None) -> dict:
        """Send command to local API."""
        method = "GET"
        if params:
            method = "PUT"

        url = f"{API_HTTP_PROTOCOL}://{self.server_host}:{self.server_port}\
            {API_PATH_MAPPING[command]}"
        _LOGGER.info("Calling %s with method %s", url, method)
        _LOGGER.debug("... and Parameters: %s", params)
        if method == "GET":
            try:
                async with self.__get_session().get(url) as resp:
                    if resp.status != 200:
                        error = f"Incorrect status code received {resp.status}"
                        _LOGGER.error(error)
                        await self.close()
                        raise PyPetWALKInvalidResponseStatus(error)
                    return await resp.json()  # type: ignore[no-any-return]
            except ClientConnectorError as ex:
                _LOGGER.error("%s", ex)
                await self.close()
                raise PyPetWALKClientConnectionError(ex) from ex

        elif method == "PUT":
            try:
                async with self.__get_session().put(url, json=params) as resp:
                    if resp.status != 202:  # Currently, API returns only 202
                        error = f"Incorrect status code received {resp.status}"
                        _LOGGER.error(error)
                        await self.close()
                        raise PyPetWALKInvalidResponseStatus(error)
                    return {}
            except ClientConnectorError as ex:
                _LOGGER.debug("%s", ex)
                await self.close()
                raise PyPetWALKClientConnectionError(ex) from ex

        return {}

    def __get_session(self) -> ClientSession:
        """Return current session, recreating if it was closed."""
        if self.session.closed:
            self.session = ClientSession()

        return self.session
