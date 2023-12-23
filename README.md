# pypetwalk

<p align="center">
    <a href="https://www.petwalk.at" target="_blank"><img src="https://www.petwalk.at/downloads_public/press/pics/petWALK-logo_(en).jpg" alt="PetWALK" /></a>
</p>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypetwalk?logo=python)
[![PyPI release](https://img.shields.io/pypi/v/pypetwalk)](https://pypi.org/project/pypetwalk/)
![Release status](https://img.shields.io/pypi/status/pypetwalk)
![Build Pipeline](https://img.shields.io/github/actions/workflow/status/p0l0/pypetwalk/ci.yml)
[![codecov](https://codecov.io/gh/p0l0/pypetwalk/branch/main/graph/badge.svg?token=V5C2O6SK2O)](https://codecov.io/gh/p0l0/pypetwalk)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=f8b424)](https://github.com/pre-commit/pre-commit)
![License](https://img.shields.io/github/license/p0l0/pypetwalk)

`pypetwalk` is a Python 3 (>= 3.11) library to communicate with the petWALK.control module.

It is intended to be used in custom_component [hapetwalk](https://github.com/p0l0/hapetwalk) for [Home Assistant](https://www.home-assistant.io/).

Implementation is based on the [petWALK.control local API (beta) (1.0.0)](https://control.petwalk.solutions/doc/api/) and some reverse engineering of the internal Websocket and AWS communication.

Available functions and their implementation status:

- [x] Activate/deactivate Brightness sensor (API)
- [x] Activate/deactivate Motion In (API)
- [x] Activate/deactivate Motion Out (API)
- [x] Activate/deactivate Rfid (API)
- [x] Activate/deactivate Time (API)
- [x] Open/close door (API)
- [x] Turn on/off the door (API)
- [x] Get Device Info (Websocket)
- [ ] Factory reset (Websocket)
- [ ] _Init drive start_ (Websocket)
- [ ] Delete RFID tag (Websocket)
- [ ] Delete all RFID tags (Websocket)
- [ ] Delete Pet RFID tag (Websocket)
- [ ] Start RFID tag Learning (Websocket)
- [ ] Stop RFID tag Learning (Websocket)
- [ ] Check if RFID Tag exists (Websocket)
- [ ] Get RFID tag list (Websocket)
- [ ] Set system time (Websocket)
- [ ] Get Wlan network list (Websocket)
- [ ] Set Wlan network (Websocket)
- [ ] Scan for Wlan networks (Websocket)
- [ ] ZigBee join allowed (Websocket)
- [ ] ZigBee confirm join (Websocket)
- [ ] ZigBee list devices (Websocket)
- [ ] ZigBee name device (Websocket)
- [ ] ZigBee remove device (Websocket)
- [ ] ZigBee update (Websocket)
- [x] Update Infos (AWS)
- [x] Get Notification Settings (AWS)
- [x] Get Timeline (AWS)

