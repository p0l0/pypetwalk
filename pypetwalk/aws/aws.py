"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import logging
from types import TracebackType

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from pycognito import Cognito

from pypetwalk.const import (
    APP_VERSION,
)
from pypetwalk.exceptions import (
    PyPetWALKClientAWSAuthenticationError,
    PyPetWALKClientConnectionError,
    PyPetWALKInvalidResponseStatus,
    PyPetWALKClientAWSMissingAuthentication,
    PyPetWALKClientAWSInvalidTokens,
)

_LOGGER = logging.getLogger(__name__)


class AWS:
    """Class for handling AWS API calls."""

    def __init__(self, url: str, user_pool_id: str, client_id: str, username: str, password: str) -> None:
        """Initialize API class."""
        self.url = url
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.username = username
        self.password = password
        self.current_aws_user = None
        self.session = ClientSession()

    async def __aenter__(self) -> "AWS":
        """Start API class from context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop AWS class from context manager."""
        await self.close()

    async def close(self) -> None:
        """Wait until all sessions are closed."""
        if self.session:
            await self.session.close()

    async def authenticate(self, username: str, password: str) -> dict:
        """Authenticate against AWS Cognito"""
        user = Cognito(self.user_pool_id, self.client_id, username=username)

        try:
            user.authenticate(password=password)
            self.current_aws_user = user
        except Exception as ex:
            _LOGGER.error("%s", ex)
            await self.close()
            raise PyPetWALKClientAWSAuthenticationError(ex) from ex

        return self.current_aws_user

    async def get_aws_update_info(self) -> dict:
        """Gets Update Infos from AWS."""
        return await self.get("update_info")

    async def get_notification_settings(self) -> dict:
        """Gets Notification Settings from AWS."""
        return await self.get("notifications/settings")

    async def get_timeline(self, door_id: int, interval_days: int) -> dict:
        """Gets Timeline for specific door_id and interval_days from AWS."""
        return await self.get(f"door_events?deviceID={door_id}&intervalDays={interval_days}")

    async def get(self, path: str)-> dict:
        url = f"{self.url}/{path}"
        _LOGGER.info("Calling AWS URL %s", url)
        try:
            headers = await self.__headers()
            async with self.__get_session().get(url, headers=headers) as resp:
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

    async def __headers(self) -> dict:
        if not self.current_aws_user:
            _LOGGER.info("Missing AWS Authentication, we need to authenticate before")
            await self.authenticate(self.username, self.password)
            # error = f"Missing AWS Authentication, please authenticate first"
            # _LOGGER.error(error)
            # raise PyPetWALKClientAWSMissingAuthentication(error)

        try:
            _LOGGER.info("Check for Valid tokens, if not valid, renew")
            self.current_aws_user.check_token()
        except Exception as ex:
            _LOGGER.error("%s", ex)
            raise PyPetWALKClientAWSInvalidTokens(ex)

        headers = {
            'Authorization': self.current_aws_user.id_token,
            'UserAccess': self.current_aws_user.access_token,
            'Client-Version': APP_VERSION
        }

        return headers

    def __get_session(self) -> ClientSession:
        """Return current session, recreating if it was closed."""
        if self.session.closed:
            self.session = ClientSession()

        return self.session
