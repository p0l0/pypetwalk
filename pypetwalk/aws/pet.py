"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

import datetime


class Pet:
    """Class that represents a Pet."""

    def __init__(
        self,
        pet_id: str = "",
        name: str | None = None,
        species: str | None = None,
        config: dict | None = None,
        created: int | None = None,
    ):
        """Initialize Pet Object."""
        self._id = pet_id
        self._name = name
        self._species = species
        self._created = datetime.datetime.fromtimestamp(0)
        self._config_in = None
        self._config_out = None

        if config is not None:
            if "in" in config:
                self._config_in = config["in"]
            if "out" in config:
                self._config_out = config["out"]

        if created is not None:
            self.set_created_from_timestamp(created)

    @property
    def id(self) -> str:
        """Return the current pet ID."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def name(self) -> str | None:
        """Return the current pet Name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def species(self) -> str | None:
        """Return the current pet Species."""
        return self._species

    @species.setter
    def species(self, value: str) -> None:
        self._species = value

    @property
    def config_in(self) -> str | None:
        """Return the current pet Entry Configuration."""
        return self._config_in

    @config_in.setter
    def config_in(self, value: str) -> None:
        self._config_in = value

    @property
    def config_out(self) -> str | None:
        """Return the current pet Out Configuration."""
        return self._config_out

    @config_out.setter
    def config_out(self, value: str) -> None:
        self._config_out = value

    @property
    def created(self) -> datetime.datetime:
        """Return the current pet Creation Datetime."""
        return self._created

    @created.setter
    def created(self, date: datetime.datetime) -> None:
        self._created = date

    def set_created_from_timestamp(self, timestamp: int) -> None:
        """Set created from timestamp."""
        date = datetime.datetime.fromtimestamp(timestamp)
        self.created = date
