"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import logging
from types import TracebackType

from .api import API
from .aws import AWS, Event, Pet
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
    AWS_CLIENT_ID,
    AWS_TIMELINE_INTEVAL_DAYS,
    AWS_URL,
    AWS_USER_POOL_ID,
    EVENT_TYPE_OPEN,
    WS_PORT,
)
from .exceptions import PyPetWALKInvalidResponse, PyPetWALKInvalidResponseValue
from .ws import WS

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


class PyPetWALK:
    """Class for communicate with the petWALK.control module."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        api_port: int = API_PORT,
        ws_port: int = WS_PORT,
        aws_url: str = AWS_URL,
        aws_user_pool_id: str = AWS_USER_POOL_ID,
        aws_client_id: str = AWS_CLIENT_ID,
    ) -> None:
        """Initialize pyPetWALK Class."""
        self.websocket_client = WS(host, ws_port)
        self.api_client = API(host, api_port)
        self.aws_client = AWS(
            aws_url, aws_user_pool_id, aws_client_id, username, password
        )

    async def __aenter__(self) -> PyPetWALK:
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
        await self.aws_client.close()

    async def get_api_data(self) -> dict[str, bool]:
        """Get all Data from Local API."""
        modes = await self.get_modes()
        states = await self.get_states()
        merged = modes | states

        result = {}
        for key, value in merged.items():
            if value in API_STATE_MAPPING:
                result[key] = API_STATE_MAPPING[value]  # type: ignore[index]
            elif isinstance(value, bool):
                result[key] = value

        return result

    async def get_modes(self) -> dict[str, bool]:
        """Return the Modes for our Door."""
        try:
            return await self.api_client.get_modes()
        finally:
            await self.api_client.close()

    async def get_states(self) -> dict[str, str]:
        """Return the States for our Door."""
        try:
            return await self.api_client.get_states()
        finally:
            await self.api_client.close()

    async def get_device_id(self) -> int:
        """Return the Device ID for our Door."""
        try:
            update_info = await self.get_aws_update_info()
            return int(update_info["update_states"][0]["deviceId"])
        except (IndexError, KeyError) as ex:
            raise PyPetWALKInvalidResponse from ex

    async def get_device_name(self) -> str:
        """Return the Device Name for our Door."""
        try:
            device_info = await self.get_device_info()
            return device_info["responses"][0]["DeviceInfo"][0]["device_name"]  # type: ignore[no-any-return] # noqa: E501
        except (IndexError, KeyError) as ex:
            raise PyPetWALKInvalidResponse from ex

    async def get_available_pets(self) -> list[Pet]:
        """Return list of available Pets."""
        try:
            device_info = await self.get_device_info()

            pets = []
            for pet in device_info["responses"][0]["DeviceInfo"][0]["pets"]:
                if pet[1] is None:
                    continue
                pets.append(
                    Pet(
                        pet_id=pet[0],
                        name=pet[1],
                        species=pet[2],
                        config=pet[3],
                        created=pet[4],
                    )
                )
            return pets
        except (IndexError, KeyError) as ex:
            raise PyPetWALKInvalidResponse from ex

    async def get_pet_status(self, door_id: int) -> dict[str, Event]:
        """Return current Pet's status."""
        timeline = await self.get_timeline(door_id, 1)

        status: dict[str, Event] = {}
        for entry in timeline:
            event = Event(entry)
            if event.event_type != EVENT_TYPE_OPEN or event.pet is None:
                continue

            pet_id = event.pet.id
            if pet_id not in status or status[pet_id].date < event.date:
                status[pet_id] = event
                continue

        return status

    async def set_brightness_sensor(self, state: bool) -> bool:
        """Set new value for brightness sensor."""
        try:
            return await self.set_state(API_STATE_BRIGHTNESS_SENSOR, state)
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
        try:
            return await self.set_state(API_STATE_MOTION_IN, state)
        finally:
            await self.api_client.close()

    async def get_motion_in(self) -> bool:
        """Get value for the 'motion in' mode."""
        try:
            return await self.__api_get_state(API_STATE_MOTION_IN)
        finally:
            await self.api_client.close()

    async def set_motion_out(self, state: bool) -> bool:
        """Set new value for 'motion out' mode."""
        try:
            return await self.set_state(API_STATE_MOTION_OUT, state)
        finally:
            await self.api_client.close()

    async def get_motion_out(self) -> bool:
        """Get value for the 'motion out' mode."""
        try:
            return await self.__api_get_state(API_STATE_MOTION_OUT)
        finally:
            await self.api_client.close()

    async def set_rfid(self, state: bool) -> bool:
        """Set new value for rfid mode."""
        try:
            return await self.set_state(API_STATE_RFID, state)
        finally:
            await self.api_client.close()

    async def get_rfid(self) -> bool:
        """Get value for the rfid mode."""
        try:
            return await self.__api_get_state(API_STATE_RFID)
        finally:
            await self.api_client.close()

    async def set_time(self, state: bool) -> bool:
        """Set new value for time mode."""
        try:
            return await self.set_state(API_STATE_TIME, state)
        finally:
            await self.api_client.close()

    async def get_time(self) -> bool:
        """Get value for the time mode."""
        try:
            return await self.__api_get_state(API_STATE_TIME)
        finally:
            await self.api_client.close()

    async def set_door_state(self, state: bool) -> bool:
        """Open or closes petWALK door."""
        try:
            return await self.set_state(API_STATE_DOOR, state)
        finally:
            await self.api_client.close()

    async def get_door_state(self) -> bool:
        """Get the current door state."""
        try:
            return await self.__api_get_state(API_STATE_DOOR)
        finally:
            await self.api_client.close()

    async def set_system_state(self, state: bool) -> bool:
        """Turn petWALK on or off."""
        try:
            return await self.set_state(API_STATE_SYSTEM, state)
        finally:
            await self.api_client.close()

    async def get_system_state(self) -> bool:
        """Get current petWALK system state."""
        try:
            return await self.__api_get_state(API_STATE_SYSTEM)
        finally:
            await self.api_client.close()

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

    async def set_state(self, param: str, value: bool) -> bool:
        """Call API method to set new value for requested mode/state."""
        try:
            method = f"set_{API_METHOD_MAPPING[param].lower()}"
            _LOGGER.debug(
                "Calling API method %s for %s with value %r", method, param, value
            )
            await getattr(self.api_client, method)(param, value)
            return True
        finally:
            await self.api_client.close()

    async def get_device_info(self) -> dict:
        """Get current device information."""
        try:
            return await self.websocket_client.device_info()
        finally:
            await self.websocket_client.close()

    async def get_aws_update_info(self) -> dict:
        """Get Update Infos from AWS."""
        try:
            return await self.aws_client.get_aws_update_info()
        finally:
            await self.aws_client.close()

    async def get_notification_settings(self) -> dict:
        """Get Notification Settings from AWS."""
        try:
            return await self.aws_client.get_notification_settings()
        finally:
            await self.aws_client.close()

    async def get_timeline(
        self, door_id: int, interval_days: int = AWS_TIMELINE_INTEVAL_DAYS
    ) -> dict:
        """Get Timeline for specific door_id and interval_days from AWS."""
        try:
            return await self.aws_client.get_timeline(door_id, interval_days)
        finally:
            await self.aws_client.close()
