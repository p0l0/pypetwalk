"""Test for pypetwalk."""
from __future__ import annotations

import json

from aiohttp import WSMsgType, web
import pytest

from pypetwalk import PyPetWALK
from pypetwalk.const import (
    API_PATH_MAPPING,
    API_PORT,
    API_STATE_BRIGHTNESS_SENSOR,
    API_STATE_DOOR,
    API_STATE_MOTION_IN,
    API_STATE_MOTION_OUT,
    API_STATE_RFID,
    API_STATE_SYSTEM,
    API_STATE_TIME,
    WS_PORT,
)


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
    aiohttp_server: any, fake_api: "FakeAPI", command: str, call_method: str
) -> None:
    """Test API set methods with activation."""
    # fake_api = FakeAPI()

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
    client = PyPetWALK(server.host, api_port=server.port)

    response = await getattr(client, call_method)(True)
    assert response is True, "Received invalid response"
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
    aiohttp_server: any, fake_api: "FakeAPI", command: str, call_method: str
) -> None:
    """Test API set methods with deactivation."""
    # fake_api = FakeAPI()

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
    client = PyPetWALK(server.host, api_port=server.port)

    response = await getattr(client, call_method)(False)
    assert response is True, "Received invalid response"
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
    aiohttp_server: any, fake_api: "FakeAPI", command: str, call_method: str
) -> None:
    """Test API get methods with activated mode."""
    # fake_api = FakeAPI()

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
    client = PyPetWALK(server.host, api_port=server.port)

    response = await getattr(client, call_method)()
    assert response is True, "Received invalid response"
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
    aiohttp_server: any, fake_api: "FakeAPI", command: str, call_method: str
) -> None:
    """Test API get methods with deactivated mode."""
    # fake_api = FakeAPI()

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
    client = PyPetWALK(server.host, api_port=server.port)

    response = await getattr(client, call_method)()
    assert response is False, "Received invalid response"
    await server.close()


@pytest.mark.asyncio
async def test_host():
    """Test initialize with host."""
    host = "127.0.0.1"
    client = PyPetWALK(host)
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
    client = PyPetWALK(host, api_port=port)
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
    client = PyPetWALK(host, ws_port=port)
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
    client = PyPetWALK(host, ws_port=ws_port, api_port=api_port)
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
    client = PyPetWALK(server.host, ws_port=server.port)
    resp = await client.get_device_info()

    assert resp == device_info["response"], "Invalid JSON Response from WS"

    await server.close()
