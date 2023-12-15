from __future__ import annotations

import datetime


class Pet(object):

    def __init__(self, id: str = None, name: str = None, species: str = None, config: dict = None, created: int = None):
        self._id = id
        self._name = name
        self._species = species

        if config is not None:
            if 'in' in config:
                self._config_in = config['in']
            if 'out' in config:
                self._config_out = config['out']

        if created is not None:
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
    def species(self) -> str:
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

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


