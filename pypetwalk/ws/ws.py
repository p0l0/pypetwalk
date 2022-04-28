"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import json
import logging
from types import TracebackType

import aiohttp

from pypetwalk.const import (
    WS_COMMAND_DEVICE_INFO,
    WS_COMMAND_FACTORY_RESET,
    WS_COMMAND_INIT_DRIVE_START,
    WS_COMMAND_RFID_DELETE,
    WS_COMMAND_RFID_DELETE_ALL,
    WS_COMMAND_RFID_DELETE_PET,
    WS_COMMAND_RFID_START_LEARN,
    WS_COMMAND_RFID_STOP_LEARN,
    WS_COMMAND_RFID_TAG_EXISTS,
    WS_COMMAND_RFID_TAG_LIST,
    WS_COMMAND_TIME_SET,
    WS_COMMAND_WIFI_NETWORK_LIST,
    WS_COMMAND_WIFI_NETWORK_SET,
    WS_COMMAND_WIFI_SCAN,
    WS_COMMAND_ZIGBEE_JOIN_ALLOWED,
    WS_COMMAND_ZIGBEE_JOIN_CONFIRM,
    WS_COMMAND_ZIGBEE_LIST_DEVICES,
    WS_COMMAND_ZIGBEE_NAME_DEVICE,
    WS_COMMAND_ZIGBEE_REMOVE_DEVICE,
    WS_COMMAND_ZIGBEE_UPDATE,
    ZIGBEE_DEFAULT_JOIN_TYPE,
)

from .request import Request

_LOGGER = logging.getLogger(__name__)


class WS:
    """Class for Websocket communication."""

    def __init__(self, host: str, port: int) -> None:
        """Initialize Websocket Class."""
        self.server_host = host
        self.server_port = port
        self.session = aiohttp.ClientSession()

    async def __aenter__(self) -> "WS":
        """Start Websocket class from context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop Websocket class from context manager."""
        await self.close()

    async def close(self) -> None:
        """Wait until all sessions are closed."""
        if self.session:
            await self.session.close()

    async def rfid_start_learn(self, slot: int) -> dict:
        """Start RFID learning process."""
        return await self.send_command(WS_COMMAND_RFID_START_LEARN, [slot])

    # @todo - Undocumented! - Need to find out correct parameters
    async def rfid_stop_learn(self) -> dict:
        """Stop RFID learning process."""
        return await self.send_command(WS_COMMAND_RFID_STOP_LEARN, [])

    async def rfid_delete(self, idx: int) -> dict:
        """Delete given RFID entry."""
        return await self.send_command(WS_COMMAND_RFID_DELETE, [idx])

    async def rfid_delete_all(self) -> dict:
        """Delete all RFID entries."""
        return await self.send_command(WS_COMMAND_RFID_DELETE_ALL, [])

    async def rfid_delete_pet(self, pet_id: str) -> dict:
        """Delete RFID based on petId."""
        return await self.send_command(WS_COMMAND_RFID_DELETE_PET, [pet_id])

    async def rfid_tag_list(self) -> dict:
        """Get list of current RFIDs."""
        return await self.send_command(WS_COMMAND_RFID_TAG_LIST, [])

    # @todo - Undocumented! - Need to find out correct parameters
    async def rfid_tag_exists(self) -> dict:
        """Check if RFID exists."""
        return await self.send_command(WS_COMMAND_RFID_TAG_EXISTS, [])

    async def zig_bee_list_devices(self) -> dict:
        """List ZigBee Devices."""
        return await self.send_command(WS_COMMAND_ZIGBEE_LIST_DEVICES, [])

    async def zig_bee_remove_device(self, component_id: str) -> dict:
        """Remove ZigBee Device."""
        return await self.send_command(WS_COMMAND_ZIGBEE_REMOVE_DEVICE, [component_id])

    async def zig_bee_start_join(self, z_type: str) -> dict:
        """Start ZigBee joining session."""
        if not z_type:
            z_type = ZIGBEE_DEFAULT_JOIN_TYPE
        return await self.send_command(
            WS_COMMAND_ZIGBEE_JOIN_ALLOWED, ["start", z_type]
        )

    async def zig_bee_get_join_status(self) -> dict:
        """Check current ZigBee joining status."""
        return await self.send_command(WS_COMMAND_ZIGBEE_JOIN_ALLOWED, [])

    async def zig_bee_join_confirm(self, component_id: str) -> dict:
        """Confirm ZigBee join for given component."""
        return await self.send_command(WS_COMMAND_ZIGBEE_JOIN_CONFIRM, [component_id])

    # @todo - Undocumented! - Need to find out correct parameters
    async def zig_bee_update(self) -> dict:
        """Update ZigBee status."""
        return await self.send_command(WS_COMMAND_ZIGBEE_UPDATE, [])

    async def zig_bee_name_device(self, component_id: str, name: str) -> dict:
        """Set name for ZigBee Device."""
        return await self.send_command(
            WS_COMMAND_ZIGBEE_NAME_DEVICE, [component_id, name]
        )

    async def device_info(self) -> dict:
        """Get current device information."""
        return await self.send_command(WS_COMMAND_DEVICE_INFO, [])

    async def wifi_network_list(self) -> dict:
        """Get Wifi network list."""
        return await self.send_command(WS_COMMAND_WIFI_NETWORK_LIST, [])

    async def wifi_network_set(
        self,
        selected_wifi: str,
        wifi_password: str,
    ) -> dict:
        """Set Wifi network."""
        return await self.send_command(
            WS_COMMAND_WIFI_NETWORK_SET, [selected_wifi, wifi_password, False]
        )

    # @todo - Undocummented! - Need to find out correct parameters
    async def wifi_scan(self) -> dict:
        """Start Wifi scan."""
        return await self.send_command(WS_COMMAND_WIFI_SCAN, [])

    # @todo - Time format is undocumented!
    async def time_set(self, time: str) -> dict:
        """Set given time."""
        return await self.send_command(WS_COMMAND_TIME_SET, [time])

    async def factory_reset(self) -> dict:
        """Reset the device to factory settings."""
        _LOGGER.warning("Factory reset was triggered!")
        return await self.send_command(WS_COMMAND_FACTORY_RESET, [])

    async def init_drive_start(self) -> dict:
        """Init drive start for the device."""
        _LOGGER.warning("Init Drive Start was triggered!")
        return await self.send_command(WS_COMMAND_INIT_DRIVE_START, [])

    async def send_command(self, command: str, params: list) -> dict:
        """Send command to local Websocket."""
        request = Request().build_request(command, params)

        url = f"ws://{self.server_host}:{self.server_port}"
        async with self.session.ws_connect(url) as websocket_connection:
            await websocket_connection.send_str(request.get_json())

            async for msg in websocket_connection:
                if msg.type == aiohttp.WSMsgType.ERROR:
                    _LOGGER.error("Unable to connect to WS %s", url)
                    result = {}
                else:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        result = json.loads(msg.data)
                return result
        return {}
