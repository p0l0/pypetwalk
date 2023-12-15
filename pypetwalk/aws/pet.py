from __future__ import annotations

import datetime


class Pet:

    def __init__(self, id: str, name: str, pet_type: str, config: dict, created: int):
        self._id = id
        self._name = name
        self._pet_type = pet_type
        if 'in' in config:
            self._config_in = config['in']
        if 'out' in config:
            self._config_out = config['out']
        self.created = created

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def pet_type(self) -> str:
        return self._pet_type

    @pet_type.setter
    def pet_type(self, value):
        self._pet_type = value

    @property
    def config_in(self) -> str:
        return self._config_in

    @config_in.setter
    def config_in(self, value):
        self._config_in = value

    @property
    def config_out(self) -> str:
        return self._config_out

    @config_out.setter
    def config_out(self, value):
        self._config_out = value

    @property
    def created(self) -> datetime.datetime:
        return self._created

    @created.setter
    def created(self, timestamp: int):
        date = datetime.datetime.fromtimestamp(timestamp)
        self._created = date


