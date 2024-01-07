"""Test for pypetwalk."""
from __future__ import annotations

from datetime import UTC, datetime, timezone
import json

from aiohttp import WSMsgType, web
import pytest

from pypetwalk import PyPetWALK
from pypetwalk.aws import Event, Pet
from pypetwalk.const import (
    API_METHOD_MAPPING,
    API_PATH_MAPPING,
    API_PORT,
    API_STATE_BRIGHTNESS_SENSOR,
    API_STATE_DOOR,
    API_STATE_MOTION_IN,
    API_STATE_MOTION_OUT,
    API_STATE_RFID,
    API_STATE_SYSTEM,
    API_STATE_TIME,
    PET_SPECIES_MAPPING,
    UNKNOWN_PET_ID,
    UNKNOWN_PET_NAME,
    WS_COMMAND_RFID_START_LEARN,
    WS_PORT,
)
from pypetwalk.exceptions import (
    BasePyPetWALKException,
    PyPetWALKClientConnectionError,
    PyPetWALKInvalidResponse,
    PyPetWALKInvalidResponseStatus,
    PyPetWALKInvalidResponseValue,
)
from pypetwalk.ws import Request

from .conftest import FakeAPI


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, call_method",
    [
        (API_STATE_BRIGHTNESS_SENSOR, "set_brightness_sensor"),
        (API_STATE_MOTION_IN, "set_motion_in"),
        (API_STATE_MOTION_OUT, "set_motion_out"),
        (API_STATE_RFID, "set_rfid"),
        (API_STATE_TIME, "set_time"),
        (API_STATE_DOOR, "set_door_state"),
        (API_STATE_SYSTEM, "set_system_state"),
    ],
)
async def test_set_values_activate(
    aiohttp_server: any, fake_api: FakeAPI, command: str, call_method: str
) -> None:
    """Test API set methods with activation."""

    async def handler(request: web.Request) -> web.Response:
        data = await request.json()
        assert request.path == fake_api.get_path(command), "Incorrect URL path called"
        assert data[command] == fake_api.get_expected_activated_value(
            command
        ), "Incorrect parameter in request"
        return web.json_response({}, status=202)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.put(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    await getattr(client, call_method)(True)
    await server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, call_method",
    [
        (API_STATE_BRIGHTNESS_SENSOR, "set_brightness_sensor"),
        (API_STATE_MOTION_IN, "set_motion_in"),
        (API_STATE_MOTION_OUT, "set_motion_out"),
        (API_STATE_RFID, "set_rfid"),
        (API_STATE_TIME, "set_time"),
        (API_STATE_DOOR, "set_door_state"),
        (API_STATE_SYSTEM, "set_system_state"),
    ],
)
async def test_set_values_deactivate(
    aiohttp_server: any, fake_api: FakeAPI, command: str, call_method: str
) -> None:
    """Test API set methods with deactivation."""

    async def handler(request: web.Request) -> web.Response:
        data = await request.json()
        assert request.path == fake_api.get_path(command), "Incorrect URL path called"
        assert data[command] == fake_api.get_expected_deactivated_value(
            command
        ), "Incorrect parameter in request"
        return web.json_response({}, status=202)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.put(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    await getattr(client, call_method)(False)
    await server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, call_method",
    [
        (API_STATE_BRIGHTNESS_SENSOR, "get_brightness_sensor"),
        (API_STATE_MOTION_IN, "get_motion_in"),
        (API_STATE_MOTION_OUT, "get_motion_out"),
        (API_STATE_RFID, "get_rfid"),
        (API_STATE_TIME, "get_time"),
        (API_STATE_DOOR, "get_door_state"),
        (API_STATE_SYSTEM, "get_system_state"),
    ],
)
async def test_get_values_activated(
    aiohttp_server: any, fake_api: FakeAPI, command: str, call_method: str
) -> None:
    """Test API get methods with activated mode."""

    async def handler(request: web.Request) -> web.Response:
        assert request.path == fake_api.get_path(command), "Incorrect URL path called"

        json_response = fake_api.get_activated_json(command)
        if not json_response:
            return web.json_response({}, status=404)

        return web.json_response(json_response, status=200)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.get(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    await getattr(client, call_method)()
    await server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, call_method",
    [
        (API_STATE_BRIGHTNESS_SENSOR, "get_brightness_sensor"),
        (API_STATE_MOTION_IN, "get_motion_in"),
        (API_STATE_MOTION_OUT, "get_motion_out"),
        (API_STATE_RFID, "get_rfid"),
        (API_STATE_TIME, "get_time"),
        (API_STATE_DOOR, "get_door_state"),
        (API_STATE_SYSTEM, "get_system_state"),
    ],
)
async def test_get_values_deactivated(
    aiohttp_server: any, fake_api: FakeAPI, command: str, call_method: str
) -> None:
    """Test API get methods with deactivated mode."""

    async def handler(request: web.Request) -> web.Response:
        assert request.path == fake_api.get_path(command), "Incorrect URL path called"

        json_response = fake_api.get_deactivated_json(command)
        if not json_response:
            return web.json_response({}, status=404)

        return web.json_response(json_response, status=200)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.get(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    await getattr(client, call_method)()
    await server.close()


@pytest.mark.asyncio
async def test_host():
    """Test initialize with host."""
    host = "127.0.0.1"
    client = PyPetWALK(host, username="username", password="password")
    assert client.websocket_client.server_host == host, "Incorrect host value at WS"
    assert (
        client.websocket_client.server_port == WS_PORT
    ), "Incorrect default port value at WS"
    assert client.api_client.server_host == host, "Incorrect host value at API"
    assert (
        client.api_client.server_port == API_PORT
    ), "Incorrect default port value at API"


@pytest.mark.asyncio
async def test_host_with_api_port():
    """Test initialize with host and API port."""
    host = "127.0.0.1"
    port = 98765
    client = PyPetWALK(host, api_port=port, username="username", password="password")
    assert client.websocket_client.server_host == host, "Incorrect host value at WS"
    assert (
        client.websocket_client.server_port == WS_PORT
    ), "Incorrect default port value at WS"
    assert client.api_client.server_host == host, "Incorrect host value at API"
    assert client.api_client.server_port == port, "Incorrect port value at API"


@pytest.mark.asyncio
async def test_host_with_ws_port():
    """Test initialize with host and WS port."""
    host = "127.0.0.1"
    port = 98765
    client = PyPetWALK(host, ws_port=port, username="username", password="password")
    assert client.websocket_client.server_host == host, "Incorrect host value at WS"
    assert (
        client.websocket_client.server_port == port
    ), "Incorrect default port value at WS"
    assert client.api_client.server_host == host, "Incorrect host value at API"
    assert client.api_client.server_port == API_PORT, "Incorrect port value at API"


@pytest.mark.asyncio
async def test_host_with_ports():
    """Test initialize with host, API port and WS port."""
    host = "127.0.0.1"
    ws_port = 98765
    api_port = 4563
    client = PyPetWALK(
        host,
        ws_port=ws_port,
        api_port=api_port,
        username="username",
        password="password",
    )
    assert client.websocket_client.server_host == host, "Incorrect host value at WS"
    assert (
        client.websocket_client.server_port == ws_port
    ), "Incorrect default port value at WS"
    assert client.api_client.server_host == host, "Incorrect host value at API"
    assert client.api_client.server_port == api_port, "Incorrect port value at API"


@pytest.mark.asyncio
async def test_ws_get_device_info(aiohttp_server: any, device_info: any) -> None:
    """Test WS deviceInfo method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_device_info()

    assert resp == device_info["response"], "Invalid JSON Response from WS"

    await server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "call_method, param",
    [
        ("get_brightness_sensor", None),
        ("set_brightness_sensor", True),
        ("get_device_info", None),
    ],
)
async def test_client_connection_error_exception(
    call_method: str, param: bool | None
) -> None:
    """Test ClientConnectionError Exception."""
    client = PyPetWALK("999.999.999.999", username="username", password="password")
    with pytest.raises(PyPetWALKClientConnectionError):
        if param is not None:
            await getattr(client, call_method)(param)
        else:
            await getattr(client, call_method)()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "call_method, json_response, exception",
    [
        ("get_brightness_sensor", {"invalid": "response"}, PyPetWALKInvalidResponse),
        (
            "get_brightness_sensor",
            {"brightnessSensor": "invalid"},
            PyPetWALKInvalidResponseValue,
        ),
    ],
)
async def test_invalid_response_exceptions(
    aiohttp_server: any,
    call_method: str,
    json_response: dict,
    exception: BasePyPetWALKException,
) -> None:
    """Test exceptions for invalid responses."""

    async def handler(request: web.Request) -> web.Response:
        return web.json_response(json_response, status=200)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.get(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    with pytest.raises(exception):
        await getattr(client, call_method)()

    await server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "call_method, param",
    [("get_brightness_sensor", None), ("set_brightness_sensor", True)],
)
async def test_http_errors(
    aiohttp_server: any,
    call_method: str,
    param: bool | None,
) -> None:
    """Test invalid HTTP Response."""

    async def handler(request: web.Request) -> web.Response:
        return web.json_response({}, status=400)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.get(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    with pytest.raises(PyPetWALKInvalidResponseStatus):
        if param is None:
            await getattr(client, call_method)()
        else:
            await getattr(client, call_method)(param)

    await server.close()


def test_ws_request_object(ws_request_data, ws_request_json):
    """Test Websocket Request object."""
    request = Request()
    request.build_request(WS_COMMAND_RFID_START_LEARN, [1])
    assert request.get_data() == ws_request_data
    assert request.get_json() == ws_request_json


@pytest.mark.asyncio
async def test_get_api_data(aiohttp_server: any, fake_api: FakeAPI) -> None:
    """Test API set methods with activation."""

    async def handler(request: web.Request) -> web.Response:
        json_response = fake_api.get_activated_json_for_path(request.path)
        if not json_response:
            return web.json_response({}, status=404)

        return web.json_response(json_response, status=200)

    app = web.Application()
    for path in API_PATH_MAPPING.values():
        app.add_routes([web.get(path, handler)])

    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, api_port=server.port, username="username", password="password"
    )

    data = await client.get_api_data()
    for key in API_METHOD_MAPPING:
        assert key in data.keys(), f"Missing key '{key}'"
        assert isinstance(data[key], bool), f"Unexpected value for {key}: '{data[key]}'"

    await server.close()


@pytest.mark.asyncio
async def test_get_device_name(aiohttp_server: any, device_info: any) -> None:
    """Test get_device_name method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_device_name()

    assert (
        resp == device_info["response"]["responses"][0]["DeviceInfo"][0]["device_name"]
    ), "Invalid JSON Response from WS"

    await server.close()


@pytest.mark.asyncio
async def test_get_sw_version(aiohttp_server: any, device_info: any) -> None:
    """Test get_sw_version method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_sw_version()

    expected = device_info["response"]["responses"][0]["DeviceInfo"][0][
        "sw_version"
    ].split(".")
    expected.pop(0)
    expected = ".".join(expected)

    assert resp == expected, "Invalid JSON Response from WS"

    await server.close()


@pytest.mark.asyncio
async def test_get_serial_number(aiohttp_server: any, device_info: any) -> None:
    """Test get_serial_number method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_serial_number()

    assert (
        resp == device_info["response"]["responses"][0]["DeviceInfo"][0]["serial"]
    ), "Invalid JSON Response from WS"

    await server.close()


@pytest.mark.asyncio
async def test_get_available_pets(aiohttp_server: any, device_info: any) -> None:
    """Test get_available_pets method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_available_pets()

    expected_pets = []
    for pet in device_info["response"]["responses"][0]["DeviceInfo"][0]["pets"]:
        if pet[1] is None:
            continue
        expected_pets.append(
            Pet(
                pet_id=pet[0],
                name=pet[1],
                species=pet[2],
                config=pet[3],
                created=pet[4],
            )
        )

    assert len(resp) == len(expected_pets), "Incorrect number of Pets in response"
    assert isinstance(resp[0], Pet), "No Pet found in response"
    for i, pet in enumerate(resp):
        assert pet.id == expected_pets[i].id, f"Invalid Pet ID for response number {i}"
        assert (
            pet.name == expected_pets[i].name
        ), f"Invalid Pet Name for response number {i}"
        assert (
            pet.species == expected_pets[i].species
        ), f"Invalid Pet Species for response number {i}"
        assert (
            pet.config_in == expected_pets[i].config_in
        ), f"Invalid Pet config_in for response number {i}"
        assert (
            pet.config_out == expected_pets[i].config_out
        ), f"Invalid Pet config_out for response number {i}"
        assert (
            pet.created == expected_pets[i].created
        ), f"Invalid Pet Created for response number {i}"
        assert (
            pet.unknown == expected_pets[i].unknown
        ), f"Invalid Pet Unknown Parameter for response number {i}"

    await server.close()


@pytest.mark.asyncio
async def test_get_available_pets_with_unknown(
    aiohttp_server: any, device_info: any
) -> None:
    """Test get_available_pets method."""

    async def handler(request: web.Request) -> web.WebSocketResponse:
        websocket_client = web.WebSocketResponse()
        await websocket_client.prepare(request)

        async for msg in websocket_client:
            if msg.type != WSMsgType.TEXT:
                pytest.raises("Invalid WS message type received")
            data = json.loads(msg.data)

            assert (
                data["requests"][0]["function"] == device_info["command"]
            ), "Invalid WS command received"

            await websocket_client.send_str(json.dumps(device_info["response"]))
            await websocket_client.close()

    app = web.Application()
    app.add_routes([web.get("/", handler)])
    server = await aiohttp_server(app)
    client = PyPetWALK(
        server.host, ws_port=server.port, username="username", password="password"
    )
    resp = await client.get_available_pets(True)

    expected_pets = []
    for pet in device_info["response"]["responses"][0]["DeviceInfo"][0]["pets"]:
        if pet[1] is None:
            continue
        expected_pets.append(
            Pet(
                pet_id=pet[0],
                name=pet[1],
                species=pet[2],
                config=pet[3],
                created=pet[4],
            )
        )
    expected_pets.append(
        Pet(
            pet_id=UNKNOWN_PET_ID,
            name=UNKNOWN_PET_NAME,
            unknown=True,
        )
    )

    assert len(resp) == len(expected_pets), "Incorrect number of Pets in response"
    assert isinstance(resp[0], Pet), "No Pet found in response"
    for i, pet in enumerate(resp):
        assert pet.id == expected_pets[i].id, f"Invalid Pet ID for response number {i}"
        assert (
            pet.name == expected_pets[i].name
        ), f"Invalid Pet Name for response number {i}"
        assert (
            pet.species == expected_pets[i].species
        ), f"Invalid Pet Species for response number {i}"
        assert (
            pet.config_in == expected_pets[i].config_in
        ), f"Invalid Pet config_in for response number {i}"
        assert (
            pet.config_out == expected_pets[i].config_out
        ), f"Invalid Pet config_out for response number {i}"
        assert (
            pet.created == expected_pets[i].created
        ), f"Invalid Pet Created for response number {i}"
        assert (
            pet.unknown == expected_pets[i].unknown
        ), f"Invalid Pet Unknown Parameter for response number {i}"

    await server.close()


def test_event_object(get_timeline: list[dict]) -> None:
    """Test Event Object."""
    for event_data in get_timeline:
        event = Event(event_data)
        assert event.id == event_data["id"], f"Error parsing event ID for {event_data}"
        assert (
            event.event_type == event_data["event_type"]
        ), f"Error parsing event Type for {event_data}"
        assert (
            event.event_source == event_data["event_source"]
        ), f"Error parsing event Source for {event_data}"
        assert (
            event.date.strftime("%Y-%m-%dT%H:%M:%S") == event_data["date"]
        ), f"Error parsing event date for {event_data}"
        assert (
            event.date.tzinfo == timezone.utc
        ), f"Incorrect timezone for event data {event_data}"

        if event_data["properties"] is not None:
            for key, value in event_data["properties"].items():
                match key:
                    case "rfid_index":
                        assert (
                            event.rfid_index == value
                        ), f"Incorrect {key} value for {event_data}"
                    case "direction":
                        assert (
                            event.direction == value
                        ), f"Incorrect {key} value for {event_data}"
                    case "localComponentId":
                        assert (
                            event.local_component_id == value
                        ), f"Incorrect {key} value for {event_data}"
                    case "pet":
                        for pet_key in event_data["properties"][key].keys():
                            match pet_key.lower():
                                case "id":
                                    assert (
                                        event.pet.id
                                        == event_data["properties"][key][pet_key]
                                    ), f"Incorrect Pet ID for {event_data}"
                                case "name":
                                    assert (
                                        event.pet.name
                                        == event_data["properties"][key][pet_key]
                                    ), f"Incorrect Pet Name for {event_data}"
                                case "species":
                                    species = event_data["properties"][key][pet_key]
                                    if isinstance(
                                        event_data["properties"][key][pet_key], int
                                    ):
                                        species = PET_SPECIES_MAPPING[
                                            event_data["properties"][key][pet_key]
                                        ]
                                    assert (
                                        event.pet.species == species
                                    ), f"Incorrect Pet Species for {event_data}"
                                case _:
                                    raise ValueError(f"Unknown Pet property: {key}")
                    case _:
                        raise ValueError(f"Unknown property: {key}")

        if event_data["pet"] is not None:
            for pet_key in event_data["pet"].keys():
                match pet_key.lower():
                    case "id":
                        assert (
                            event.pet.id == event_data["pet"][pet_key]
                        ), f"Incorrect Pet ID for {event_data}"
                    case "name":
                        assert (
                            event.pet.name == event_data["pet"][pet_key]
                        ), f"Incorrect Pet Name for {event_data}"
                    case "species":
                        species = event_data["pet"][pet_key]
                        if isinstance(event_data["pet"][pet_key], int):
                            species = PET_SPECIES_MAPPING[event_data["pet"][pet_key]]
                        assert (
                            event.pet.species == species
                        ), f"Incorrect Pet Species for {event_data}"
                    case _:
                        raise ValueError(f"Unknown Pet property: {pet_key}")


def test_pet_object(pet_object_data: list[dict]) -> None:
    """Test Pet Object."""
    for expected_pet in pet_object_data:
        pet = Pet(**expected_pet)
        assert pet.id == expected_pet["pet_id"], f"Invalid Pet ID for {expected_pet}"
        assert pet.name == expected_pet["name"], f"Invalid Pet Name for {expected_pet}"
        assert (
            pet.species == expected_pet["species"]
        ), f"Invalid Pet Species for {expected_pet}"
        assert pet.created == datetime.fromtimestamp(
            expected_pet["created"], tz=UTC
        ), f"Invalid Pet Creation Date for {expected_pet}"

        if pet.config_in:
            assert (
                pet.config_in == expected_pet["config"]["in"]
            ), f"Invalid config IN for {expected_pet}"

        if pet.config_out:
            assert (
                pet.config_out == expected_pet["config"]["out"]
            ), f"Invalid config OUT for {expected_pet}"

        if "unknown" not in expected_pet:
            assert pet.unknown is False, f"Invalid Pet Unknown for {expected_pet}"
        else:
            assert (
                pet.unknown == expected_pet["unknown"]
            ), f"Invalid Pet Unknown for {expected_pet}"


# @TODO - We need to test our new methods and the whole AWS Implementation!

# from moto import mock_cognitoidp
# @mock_cognitoidp
# @pytest.mark.asyncio
# async def test_get_aws_update_info(aiohttp_server: any, fake_api: FakeAPI) -> None:
#     """Test AWS get Update Info."""
#
#     # @TODO - Fake the AWS API!
#     async def handler(request: web.Request) -> web.Response:
#         json_response = fake_api.get_activated_json_for_path(path)
#         if not json_response:
#             return web.json_response({}, status=404)
#
#         return web.json_response(json_response, status=200)
#
#     app = web.Application()
#     for path in API_PATH_MAPPING.values():
#         app.add_routes([web.get(path, handler)])
#
#     server = await aiohttp_server(app)
#     client = PyPetWALK(
#         server.host, api_port=server.port, username="username", password="password"
#     )
#
#     await client.get_api_data()  # get_aws_update_info()
#     await server.close()
