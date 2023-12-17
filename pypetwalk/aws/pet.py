"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import datetime


class Pet:
    """Class that represents a Pet."""

    def __init__(
        self,
        pet_id: str | None = None,
        name: str | None = None,
        species: str | None = None,
        config: dict | None = None,
        created: int | None = None,
    ):
        self._id = pet_id
        self._name = name
        self._species = species

        if config is not None:
            if "in" in config:
                self._config_in = config["in"]
            if "out" in config:
                self._config_out = config["out"]

        if created is not None:
            self.created = created

    @property
    def id(self) -> str:
        """Return the current pet ID."""
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self) -> str:
        """Return the current pet Name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def species(self) -> str:
        """Return the current pet Species."""
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

    @property
    def config_in(self) -> str:
        """Return the current pet Entry Configuration."""
        return self._config_in

    @config_in.setter
    def config_in(self, value):
        self._config_in = value

    @property
    def config_out(self) -> str:
        """Return the current pet Out Configuration."""
        return self._config_out

    @config_out.setter
    def config_out(self, value):
        self._config_out = value

    @property
    def created(self) -> datetime.datetime:
        """Return the current pet Creation Datetime."""
        return self._created

    @created.setter
    def created(self, timestamp: int):
        date = datetime.datetime.fromtimestamp(timestamp)
        self._created = date
