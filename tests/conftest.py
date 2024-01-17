"""Conftest for pypetwalk."""
from __future__ import annotations

import uuid

import pytest

from pypetwalk.const import (
    API_METHOD_MAPPING,
    API_PATH_MAPPING,
    API_STATE_DOOR,
    API_STATE_MAPPING_DOOR_CLOSE,
    API_STATE_MAPPING_DOOR_CLOSED,
    API_STATE_MAPPING_DOOR_OPEN,
    API_STATE_MAPPING_SYSTEM_OFF,
    API_STATE_MAPPING_SYSTEM_ON,
    API_STATE_SYSTEM,
    WS_COMMAND_RFID_START_LEARN,
)


class FakeAPI:
    """Class for fake petWALK.control API"""

    def __init__(self):
        """Initialize FakeAPI class."""
        self.json_mode = {
            "brightnessSensor": False,
            "motion_in": False,
            "motion_out": False,
            "rfid": False,
            "time": False,
        }
        self.json_state = {
            "door": API_STATE_MAPPING_DOOR_CLOSED,
            "system": API_STATE_MAPPING_SYSTEM_ON,
        }

    def get_path(self, command: str) -> str:
        """Returns expected path for command."""
        return API_PATH_MAPPING[API_METHOD_MAPPING[command]]

    def get_command(self, path: str) -> str | None:
        """Returns command for given path."""
        for key, value in API_PATH_MAPPING.items():
            if value == path:
                return key

        return None

    def get_activated_json_for_path(self, path: str) -> dict:
        """Returns activated value for given path."""
        command = self.get_command(path)
        json_response = {}
        if command == "mode":
            json_response = self.json_mode
        elif command == "state":
            json_response = self.json_state

        return json_response

    def get_expected_activated_value(self, command: str) -> str | bool:
        """Returns expected value when activating command."""
        expected_value = True
        if command == API_STATE_SYSTEM:
            expected_value = API_STATE_MAPPING_SYSTEM_ON
        elif command == API_STATE_DOOR:
            expected_value = API_STATE_MAPPING_DOOR_OPEN

        return expected_value

    def get_expected_deactivated_value(self, command: str) -> str | bool:
        """Returns expected value when deactivating command."""
        expected_value = False
        if command == API_STATE_SYSTEM:
            expected_value = API_STATE_MAPPING_SYSTEM_OFF
        elif command == API_STATE_DOOR:
            expected_value = API_STATE_MAPPING_DOOR_CLOSE

        return expected_value

    def get_activated_json(self, command: str) -> dict:
        """Returns dict for JSON with 'command' activated."""
        json_response = {}
        if API_METHOD_MAPPING[command] == "mode":
            json_response = self.json_mode
        elif API_METHOD_MAPPING[command] == "state":
            json_response = self.json_state

        json_response[command] = True
        if command == API_STATE_SYSTEM:
            json_response[command] = API_STATE_MAPPING_SYSTEM_ON
        elif command == API_STATE_DOOR:
            json_response[command] = API_STATE_MAPPING_DOOR_OPEN

        return json_response

    def get_deactivated_json(self, command: str) -> dict:
        """Returns dict for JSON with 'command' deactivated."""
        json_response = {}
        if API_METHOD_MAPPING[command] == "mode":
            json_response = self.json_mode
        elif API_METHOD_MAPPING[command] == "state":
            json_response = self.json_state

        json_response[command] = False
        if command == API_STATE_SYSTEM:
            json_response[command] = API_STATE_MAPPING_SYSTEM_OFF
        elif command == API_STATE_DOOR:
            json_response[command] = API_STATE_MAPPING_DOOR_CLOSED

        return json_response


@pytest.fixture
def fake_api():
    """Fake API fixture."""
    return FakeAPI()


@pytest.fixture
def ws_request_data():
    """Data object fixture for WS Request."""
    return {"requests": [{"function": WS_COMMAND_RFID_START_LEARN, "params": [1]}]}


@pytest.fixture
def ws_request_json():
    """JSON String fixture for WS Request."""
    return f'{{"requests": [{{"function": "{WS_COMMAND_RFID_START_LEARN}", "params": [1]}}]}}'


@pytest.fixture
def device_info():
    """Fixture for get_device_info test."""
    return {
        "command": "DeviceInfo",
        "response": {
            "request-id": "0b482bd5-c990-4892-ad05-fbb4b5a0ef0e",
            "responses": [
                {
                    "DeviceInfo": [
                        {
                            "cfg_auc": 0,
                            "clb_cfg_battery": 1,
                            "clb_cfg_brightness": 50,
                            "clb_cfg_did": "off",
                            "clb_cfg_door_angle": 50,
                            "clb_cfg_flags": 1287,
                            "clb_cfg_led_brightness": 50,
                            "clb_cfg_open_time": 2,
                            "clb_cfg_petSetting": "[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]",
                            "clb_cfg_rest_api": 1,
                            "clb_cfg_sens_in": 80,
                            "clb_cfg_sens_out": 80,
                            "clb_cfg_sens_rain": 50,
                            "clb_cfg_time_in_off": 59,
                            "clb_cfg_time_in_on": 60,
                            "clb_cfg_time_mode": 24,
                            "clb_cfg_time_out_off": 1185,
                            "clb_cfg_time_out_on": 390,
                            "clb_cfg_timezone": "Europe/Berlin",
                            "clb_cfg_volume": 0,
                            "clb_features": {"zigbee": False},
                            "clb_state_alarm": 0,
                            "clb_state_door_pos": "closed",
                            "clb_state_error": 0,
                            "clb_state_ip": "192.168.0.10",
                            "clb_state_opmode": "on",
                            "clb_state_power": "mains",
                            "clb_state_sense_raining": "no_sensor",
                            "clb_state_version": "0.1.20",
                            "components": [
                                [
                                    "intern",
                                    "petWALK Door",
                                    None,
                                    "petwalk",
                                    "intern",
                                    "",
                                    "4.2",
                                    "1.0",
                                    None,
                                    None,
                                    None,
                                    None,
                                ]
                            ],
                            "device_name": "pw_clb_v2_12345A67B8900000",
                            "pets": [
                                [
                                    "d1c87845-c3f3-421e-9937-132744b6a801",
                                    "Garfield",
                                    "cat",
                                    {"in": "default", "out": "default"},
                                    1651098738,
                                    None,
                                ],
                                [
                                    "edd68702-0bce-46a2-a1dd-57222aba3eb1",
                                    "Tom",
                                    "cat",
                                    {"in": "default", "out": "default"},
                                    1651098739,
                                    None,
                                ],
                            ],
                            "serial": "12345A67B8900000",
                            "sw_version": "0.1.20",
                            "ws_version": "2.0.0",
                        }
                    ]
                }
            ],
            "version": "2.0.0",
        },
    }


@pytest.fixture
def update_info():
    """Fixture for update_info test."""
    return {
        "update_states": [
            {
                "deviceId": 1234,
                "componentUpdates": [],
                "currentVersion": "0.1.21",
                "targetVersion": "0.1.21",
                "description": {},
                "jobStatus": "none",
            }
        ],
        "component_update_states": None,
    }


@pytest.fixture
def get_timeline():
    """Fixture for get_timeline test."""
    return [
        {
            "id": 58755526,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": 0,
            },
            "date": "2023-12-06T19:22:26",
            "properties": {
                "rfid_index": 0,
                "direction": "OUT",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 58755540,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T19:22:43",
            "properties": {},
        },
        {
            "id": 58755636,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "45d62731-8bae-4483-9a5e-6f7404b6870a",
                "Name": "Cat2",
                "species": 0,
            },
            "date": "2023-12-06T19:24:22",
            "properties": {
                "rfid_index": 1,
                "direction": "OUT",
                "localComponentId": "intern",
                "pet": {"id": "45d62731-8bae-4483-9a5e-6f7404b6870a", "name": "Cat2"},
            },
        },
        {
            "id": 58755653,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T19:24:37",
            "properties": {},
        },
        {
            "id": 58756531,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": 0,
            },
            "date": "2023-12-06T19:45:39",
            "properties": {
                "rfid_index": 0,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 58756548,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T19:45:54",
            "properties": {},
        },
        {
            "id": 58758086,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "45d62731-8bae-4483-9a5e-6f7404b6870a",
                "Name": "Cat2",
                "species": 0,
            },
            "date": "2023-12-06T20:23:39",
            "properties": {
                "rfid_index": 1,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "45d62731-8bae-4483-9a5e-6f7404b6870a", "name": "Cat2"},
            },
        },
        {
            "id": 58758101,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T20:23:59",
            "properties": {},
        },
        {
            "id": 58758900,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": 0,
            },
            "date": "2023-12-06T20:44:58",
            "properties": {
                "rfid_index": 0,
                "direction": "OUT",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 58758916,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T20:45:16",
            "properties": {},
        },
        {
            "id": 58759430,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": 0,
            },
            "date": "2023-12-06T20:59:34",
            "properties": {
                "rfid_index": 0,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 58759439,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-06T20:59:49",
            "properties": {},
        },
        {
            "id": 58989304,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T04:35:24",
            "properties": {
                "rfid_index": "",
                "direction": "",
                "localComponentId": "intern",
            },
        },
        {
            "id": 58989311,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T04:35:41",
            "properties": {},
        },
        {
            "id": 58990656,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "45d62731-8bae-4483-9a5e-6f7404b6870a",
                "Name": "Cat2",
                "species": 0,
            },
            "date": "2023-12-11T05:17:18",
            "properties": {
                "rfid_index": 1,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "45d62731-8bae-4483-9a5e-6f7404b6870a", "name": "Cat2"},
            },
        },
        {
            "id": 58990670,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T05:17:35",
            "properties": {},
        },
        {
            "id": 59001099,
            "event_type": "off",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T08:56:26",
            "properties": {},
        },
        {
            "id": 59001180,
            "event_type": "on",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T08:58:06",
            "properties": {},
        },
        {
            "id": 59007108,
            "event_type": "offline",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T11:28:23",
            "properties": {},
        },
        {
            "id": 59007611,
            "event_type": "online",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T11:41:13",
            "properties": {},
        },
        {
            "id": 59016951,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:13:36",
            "properties": {
                "rfid_index": "",
                "direction": "",
                "localComponentId": "intern",
            },
        },
        {
            "id": 59016970,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:13:52",
            "properties": {},
        },
        {
            "id": 59017374,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:21:04",
            "properties": {
                "rfid_index": "",
                "direction": "",
                "localComponentId": "intern",
            },
        },
        {
            "id": 59017397,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:21:23",
            "properties": {},
        },
        {
            "id": 59017916,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": 0,
            },
            "date": "2023-12-11T15:29:41",
            "properties": {
                "rfid_index": 0,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 59017916,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "e64226a5-a435-4fbe-98f3-83258041e4ea",
                "Name": "Cat1",
                "species": "cat",
            },
            "date": "2023-12-11T15:29:41",
            "properties": {
                "rfid_index": 0,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "e64226a5-a435-4fbe-98f3-83258041e4ea", "name": "Cat1"},
            },
        },
        {
            "id": 59017931,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:29:56",
            "properties": {},
        },
        # Missing properties and pet keys
        {
            "id": 59017931,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:29:56",
        },
        {
            "id": 59017931,
            "event_type": "close",
            "event_source": "DOOR",
            "date": "2023-12-11T15:29:56",
            "properties": {},
        },
        {
            "id": 59017931,
            "event_type": "close",
            "event_source": "DOOR",
            "date": "2023-12-11T15:29:56",
        },
    ]


@pytest.fixture
def get_invalid_timeline():
    """Fixture for invalid get_timeline test."""
    return [
        # Invalid Entries
        {
            "id": 59017931,
            "event_type": "close",
            "event_source": "DOOR",
        },
        {
            "id": 59017931,
            "event_type": "close",
            "date": "2023-12-11T15:29:56",
        },
        {
            "id": 59017931,
            "event_source": "DOOR",
            "date": "2023-12-11T15:29:56",
        },
        {
            "event_type": "close",
            "event_source": "DOOR",
            "date": "2023-12-11T15:29:56",
        },
        {
            "id": 59017397,
            "event_type": "close",
            "event_source": "DOOR",
            "pet": None,
            "date": "2023-12-11T15:21:23",
            "properties": {
                "invalid": True,
            },
        },
        {
            "id": 58990656,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "id": "45d62731-8bae-4483-9a5e-6f7404b6870a",
                "Name": "Cat2",
                "species": 0,
            },
            "date": "2023-12-11T05:17:18",
            "properties": {
                "rfid_index": 1,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"invalid": True},
            },
        },
        {
            "id": 58990656,
            "event_type": "open",
            "event_source": "DOOR",
            "pet": {
                "invalid": True,
            },
            "date": "2023-12-11T05:17:18",
            "properties": {
                "rfid_index": 1,
                "direction": "IN",
                "localComponentId": "intern",
                "pet": {"id": "45d62731-8bae-4483-9a5e-6f7404b6870a", "name": "Cat2"},
            },
        },
    ]


@pytest.fixture
def pet_object_data():
    """Fixture for Pet Object test."""
    return [
        {
            "pet_id": uuid.uuid4(),
            "name": uuid.uuid4(),
            "species": "cat",
            "config": {},
            "created": 1651098738,
            "unknown": False,
        },
        {
            "pet_id": uuid.uuid4(),
            "name": uuid.uuid4(),
            "species": "dog",
            "config": {"in": "default", "out": "default"},
            "created": 1651098739,
            "unknown": True,
        },
        {
            "pet_id": uuid.uuid4(),
            "name": uuid.uuid4(),
            "species": "cat",
            "config": {"in": "default"},
            "created": 1651098739,
        },
        {
            "pet_id": uuid.uuid4(),
            "name": uuid.uuid4(),
            "species": "dog",
            "config": {"out": "default"},
            "created": 1651098739,
            "unknown": True,
        },
    ]
