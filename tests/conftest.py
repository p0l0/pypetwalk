"""Conftest for pypetwalk."""
from __future__ import annotations

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
