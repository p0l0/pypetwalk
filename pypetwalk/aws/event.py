"""pypetwalk is a Python library to communicate with the petWALK.control module."""
from __future__ import annotations

from datetime import datetime

from pypetwalk.const import PET_SPECIES_MAPPING

from .pet import Pet


class Event:
    """Class that represents an AWS Event."""

    _rfid_index = None
    _direction = None
    _local_component_id = None
    _pet = None

    def __init__(
        self, event: dict = None
    ):  # , id: int, event_type: str, event_source: str, date: str, pet: dict = None, properties: dict = None):
        if event is not None:
            self.id = event["id"]
            self.event_type = event["event_type"]
            self.event_source = event["event_source"]
            self.date = event["date"]

            if event["properties"] is not None:
                for key, value in event["properties"].items():
                    match key:
                        case "rfid_index":
                            self.rfid_index = value
                        case "direction":
                            self.direction = value
                        case "localComponentId":
                            self.local_component_id = value
                        case "pet":
                            self.pet = value
                        case _:
                            raise ValueError(f"Unknown property: {key}")

            if event["pet"] is not None:
                self.pet = event["pet"]

    @property
    def id(self) -> int:
        """Return the event ID."""
        return self._id

    @id.setter
    def id(self, event_id: int):
        self._id = event_id

    @property
    def event_type(self) -> str:
        """Return the event type."""
        return self._event_type

    @event_type.setter
    def event_type(self, event_type: str):
        self._event_type = event_type

    @property
    def event_source(self) -> str:
        """Return the event source."""
        return self._event_source

    @event_source.setter
    def event_source(self, event_source: str):
        self._event_source = event_source

    @property
    def pet(self) -> Pet:
        """Return the event Pet."""
        return self._pet

    @pet.setter
    def pet(self, pet_data: dict):
        pet = Pet()

        for key in pet_data.keys():
            match key.lower():
                case "id":
                    pet.id = pet_data[key]
                case "name":
                    pet.name = pet_data[key]
                case "species":
                    if isinstance(pet_data[key], int):
                        pet.species = PET_SPECIES_MAPPING[pet_data[key]]
                    else:
                        pet.species = pet_data[key]
                case _:
                    raise ValueError(f"Unknown Pet property: {key}")
        self._pet = pet

    @property
    def date(self) -> datetime:
        """Return the event date."""
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    @property
    def rfid_index(self) -> int:
        """Return the event RFID Index."""
        return self._rfid_index

    @rfid_index.setter
    def rfid_index(self, rfid_index: int):
        self._rfid_index = rfid_index

    @property
    def direction(self) -> str:
        """Return the event direction."""
        return self._direction

    @direction.setter
    def direction(self, direction: str):
        self._direction = direction

    @property
    def local_component_id(self) -> str:
        """Return the event local component ID."""
        return self._local_component_id

    @local_component_id.setter
    def local_component_id(self, local_component_id: str):
        self._local_component_id = local_component_id
