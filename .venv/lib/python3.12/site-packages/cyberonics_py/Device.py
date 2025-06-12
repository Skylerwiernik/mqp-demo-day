import json
from abc import ABC
from .graphics.GraphicCell import GraphicCell
from .DeviceProperty import DeviceProperty
from typing import Optional, Callable
from uuid import uuid4

from .graphics.GraphicState import GraphicState


class Device(ABC):
    def __init__(self, properties: [DeviceProperty], graphic_cell: Optional[GraphicCell] = None):
        super().__init__()
        self.__properties = properties
        for p in properties:
            p.add_listener(self.__got_update)
        if graphic_cell is None:
            self.graphic_cell = GraphicCell([])
        else:
            self.graphic_cell = graphic_cell
        for graphic in self.graphic_cell.graphics:
            graphic.add_graphic_listener(self.__got_update)
        self.device_cell = graphic_cell
        self.__listeners = []
        self.__uuid = uuid4()
        self.__last_state = None

    @property
    def uuid(self) -> uuid4:
        return self.__uuid

    def get_state(self) -> dict[str, any]:
        graphic_states = [graphic.get_state() for graphic in self.device_cell.graphics]
        device_state = {str(state.uuid): state.encode() for state in graphic_states}
        self.__last_state = device_state
        return device_state

    def set_state(self, state: dict[str, any] or str) -> None:
        if type(state) == str:
            state: dict[str, any] = json.loads(state)
        for graphic in self.device_cell.graphics:
            try:
                graphic_state = GraphicState.decode(state[str(graphic.uuid)])
                graphic.set_state(graphic_state)
                self.__last_state = state
            except KeyError:
                raise ValueError("Invalid state")

    """
    Adds a listener and returns its ID. This id can be passed to `free_listener` to remove the listener.
    """
    def add_listener(self, listener: Callable[['Device'], None]) -> int:
        self.__listeners.append(listener)
        return len(self.__listeners)

    """
    Removes a listener by its ID.
    """
    def free_listener(self, listener_id: int) -> None:
        if len(self.__listeners) < listener_id or listener_id < 1:
            raise ValueError("Invalid listener ID")
        self.__listeners.pop(listener_id - 1)

    def __got_update(self, _):
        if self.__last_state == self.get_state():
            print("Ignoring unchanged update for device", self.uuid)
            return
        for listener in self.__listeners:
            listener(self)