"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import logging
from types import TracebackType

from .api import API
from .const import (
    API_METHOD_MAPPING,
    API_PORT,
    API_STATE_BRIGHTNESS_SENSOR,
    API_STATE_DOOR,
    API_STATE_MAPPING,
    API_STATE_MOTION_IN,
    API_STATE_MOTION_OUT,
    API_STATE_RFID,
    API_STATE_SYSTEM,
    API_STATE_TIME,
    WS_PORT,
    AWS_URL,
    AWS_USER_POOL_ID,
    AWS_CLIENT_ID,
    AWS_TIMELINE_INTEVAL_DAYS,
)
from .exceptions import PyPetWALKInvalidResponse, PyPetWALKInvalidResponseValue
from .ws import WS

from .aws import AWS

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


class PyPetWALK:
    """Class for communicate with the petWALK.control module."""

    def __init__(
        self, host: str, username: str, password: str,
            api_port: int = API_PORT, ws_port: int = WS_PORT,
            aws_url: str = AWS_URL,
            aws_user_pool_id: str = AWS_USER_POOL_ID, aws_client_id: str = AWS_CLIENT_ID
    ) -> None:
        """Initialize pyPetWALK Class."""
        self.websocket_client = WS(host, ws_port)
        self.api_client = API(host, api_port)
        self.aws_client = AWS(aws_url, aws_user_pool_id, aws_client_id, username, password)

    async def __aenter__(self) -> "PyPetWALK":
        """Start pyPetWALK class from context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop pyPetWALK class from context manager."""
        await self.websocket_client.close()
        await self.api_client.close()

    async def get_modes(self):
        try:
            return await self.api_client.get_modes()
        finally:
            await self.api_client.close()

    async def get_states(self):
        try:
            return await self.api_client.get_states()
        finally:
            await self.api_client.close()

    async def set_brightness_sensor(self, state: bool) -> bool:
        """Set new value for brightness sensor."""
        try:
            return await self.__api_set_state(API_STATE_BRIGHTNESS_SENSOR, state)
        finally:
            await self.api_client.close()

    async def get_brightness_sensor(self) -> bool:
        """Get current value for brightness sensor."""
        try:
            return await self.__api_get_state(API_STATE_BRIGHTNESS_SENSOR)
        finally:
            await self.api_client.close()

    async def set_motion_in(self, state: bool) -> bool:
        """Set new value for 'motion in' mode."""
        return await self.__api_set_state(API_STATE_MOTION_IN, state)

    async def get_motion_in(self) -> bool:
        """Get value for the 'motion in' mode."""
        return await self.__api_get_state(API_STATE_MOTION_IN)

    async def set_motion_out(self, state: bool) -> bool:
        """Set new value for 'motion out' mode."""
        return await self.__api_set_state(API_STATE_MOTION_OUT, state)

    async def get_motion_out(self) -> bool:
        """Get value for the 'motion out' mode."""
        return await self.__api_get_state(API_STATE_MOTION_OUT)

    async def set_rfid(self, state: bool) -> bool:
        """Set new value for rfid mode."""
        return await self.__api_set_state(API_STATE_RFID, state)

    async def get_rfid(self) -> bool:
        """Get value for the rfid mode."""
        return await self.__api_get_state(API_STATE_RFID)

    async def set_time(self, state: bool) -> bool:
        """Set new value for time mode."""
        return await self.__api_set_state(API_STATE_TIME, state)

    async def get_time(self) -> bool:
        """Get value for the time mode."""
        return await self.__api_get_state(API_STATE_TIME)

    async def set_door_state(self, state: bool) -> bool:
        """Open or closes petWALK door."""
        return await self.__api_set_state(API_STATE_DOOR, state)

    async def get_door_state(self) -> bool:
        """Get the current door state."""
        return await self.__api_get_state(API_STATE_DOOR)

    async def set_system_state(self, state: bool) -> bool:
        """Turn petWALK on or off."""
        return await self.__api_set_state(API_STATE_SYSTEM, state)

    async def get_system_state(self) -> bool:
        """Get current petWALK system state."""
        return await self.__api_get_state(API_STATE_SYSTEM)

    async def __api_get_state(self, param: str) -> bool:
        """Call API method to get the request mode/state."""
        method = f"get_{API_METHOD_MAPPING[param].lower()}s"
        _LOGGER.debug("Calling API method %s for %s", method, param)
        resp = await getattr(self.api_client, method)()
        if param not in resp:
            error = f"Invalid Response {param} not found in {{resp}}"
            _LOGGER.debug(error)
            raise PyPetWALKInvalidResponse(error)

        if resp[param] is True or resp[param] is False:
            result = resp[param]
        elif resp[param] in API_STATE_MAPPING:
            result = API_STATE_MAPPING[resp[param]]
        else:
            error = f"Unknown response value {resp[param]} for {param}"
            _LOGGER.error(error)
            raise PyPetWALKInvalidResponseValue(error)

        return result  # type: ignore[no-any-return]

    async def __api_set_state(self, param: str, value: bool) -> bool:
        """Call API method to set new value for requested mode/state."""
        method = f"set_{API_METHOD_MAPPING[param].lower()}"
        _LOGGER.debug(
            "Calling API method %s for %s with value %r", method, param, value
        )
        await getattr(self.api_client, method)(param, value)
        return True

    async def get_device_info(self) -> dict:
        """Get current device information."""
        return await self.websocket_client.device_info()

    async def get_aws_update_info(self) -> dict:
        """Gets Update Infos from AWS."""
        return await self.aws_client.get_aws_update_info()

    async def get_notification_settings(self) -> dict:
        """Gets Notification Settings from AWS."""
        return await self.aws_client.get_notification_settings()

    async def get_timeline(self, door_id: int, interval_days: int = AWS_TIMELINE_INTEVAL_DAYS) -> dict:
        """Gets Timeline for specific door_id and interval_days from AWS."""
        return await self.aws_client.get_timeline(door_id, interval_days)