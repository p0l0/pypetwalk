"""Constants for the petWALK integration."""
from typing import Final

APP_VERSION: Final = "1.4.28"

API_PORT: Final = 8080
API_HTTP_PROTOCOL: Final = "http"
API_REQUEST_TIMEOUT: Final = 30
WS_PORT: Final = 1234
WS_REQUEST_TIMEOUT: Final = 30
AWS_URL: Final = "https://caln02rdoj.execute-api.eu-west-1.amazonaws.com/Master"
AWS_REQUEST_TIMEOUT: Final = 60
AWS_USER_POOL_ID: Final = "eu-west-1_NaHCncUdX"
AWS_CLIENT_ID: Final = "2qht0pl3vufdq8dmah5crv2e0o"
AWS_TIMELINE_INTEVAL_DAYS: Final = 365

WS_COMMAND_RFID_START_LEARN: Final = "RFIDStartLearn"
WS_COMMAND_RFID_STOP_LEARN: Final = "RFIDStopLearn"
WS_COMMAND_RFID_DELETE: Final = "RFIDDelete"
WS_COMMAND_RFID_DELETE_ALL: Final = "RFIDDeleteAll"
WS_COMMAND_RFID_DELETE_PET: Final = "RFIDDeletePet"
WS_COMMAND_RFID_TAG_LIST: Final = "RFIDTagList"
WS_COMMAND_RFID_TAG_EXISTS: Final = "RFIDTagExists"
WS_COMMAND_ZIGBEE_LIST_DEVICES: Final = "ZigBeeListDevices"
WS_COMMAND_ZIGBEE_REMOVE_DEVICE: Final = "ZigBeeRemoveDevice"
WS_COMMAND_ZIGBEE_JOIN_ALLOWED: Final = "ZigBeeJoinAllowed"
WS_COMMAND_ZIGBEE_NAME_DEVICE: Final = "ZigBeeNameDevice"
WS_COMMAND_ZIGBEE_UPDATE: Final = "ZigBeeUpdate"
WS_COMMAND_ZIGBEE_JOIN_CONFIRM: Final = "ZigBeeJoinConfirm"
WS_COMMAND_DEVICE_INFO: Final = "DeviceInfo"
WS_COMMAND_WIFI_NETWORK_LIST: Final = "WifiNetworkList"
WS_COMMAND_WIFI_NETWORK_SET: Final = "WifiNetworkSet"
WS_COMMAND_WIFI_SCAN: Final = "WifiScan"
WS_COMMAND_TIME_SET: Final = "TimeSet"
WS_COMMAND_FACTORY_RESET: Final = "FactoryReset"
WS_COMMAND_INIT_DRIVE_START: Final = "InitDriveStart"

ZIGBEE_DEFAULT_JOIN_TYPE: Final = "petWALK_ALB"

API_STATE_BRIGHTNESS_SENSOR: Final = "brightnessSensor"
API_STATE_MOTION_IN: Final = "motion_in"
API_STATE_MOTION_OUT: Final = "motion_out"
API_STATE_RFID: Final = "rfid"
API_STATE_TIME: Final = "time"
API_STATE_DOOR: Final = "door"
API_STATE_SYSTEM: Final = "system"

API_METHOD_MAPPING: dict[str, str] = {
    API_STATE_BRIGHTNESS_SENSOR: "mode",
    API_STATE_MOTION_IN: "mode",
    API_STATE_MOTION_OUT: "mode",
    API_STATE_RFID: "mode",
    API_STATE_TIME: "mode",
    API_STATE_DOOR: "state",
    API_STATE_SYSTEM: "state",
}

API_PATH_MAPPING: dict[str, str] = {"mode": "/modes", "state": "/states"}

API_STATE_MAPPING: dict[str, bool] = {
    "closed": False,
    "close": False,
    "open": True,
    "off": False,
    "on": True,
}

API_STATE_MAPPING_DOOR_OPEN: Final = "open"
API_STATE_MAPPING_DOOR_CLOSE: Final = "close"
API_STATE_MAPPING_DOOR_CLOSED: Final = "closed"
API_STATE_MAPPING_SYSTEM_ON: Final = "on"
API_STATE_MAPPING_SYSTEM_OFF: Final = "off"

PET_SPECIES_MAPPING: dict[int, str] = {
    0: "cat",
    1: "dog",
}

EVENT_DIRECTION_IN: Final = "IN"
EVENT_DIRECTION_OUT: Final = "OUT"

EVENT_TYPE_OPEN: Final = "open"
EVENT_TYPE_CLOSE: Final = "close"
EVENT_TYPE_ONLINE: Final = "online"
EVENT_TYPE_OFFLINE: Final = "offline"
EVENT_TYPE_ON: Final = "on"
EVENT_TYPE_OFF: Final = "off"
