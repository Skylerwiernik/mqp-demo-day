from abc import ABC, abstractmethod
from typing import Any, Optional, Callable

import uuid

from ..DeviceProperty import DeviceProperty
from .GraphicState import GraphicState


class Graphic(ABC):
    def __init__(self, managed_property: Optional[DeviceProperty[Any]]):
        self.managed_property = managed_property
        self.__uuid = uuid.uuid4()
        self.__listeners = []
        super().__init__()

    """
    Listens to visual changes of the graphic. This does *not* notify on changes to managed properties.
    You must listen to the managed property directly.
    """
    def add_graphic_listener(self, listener: Callable[['Graphic'], None]) -> None:
        self.__listeners.append(listener)


    @property
    def uuid(self) -> uuid.UUID:
        return self.__uuid


    # Called when the visual state of the graphic changes. NOT on updates to the managed property
    def _notify(self) -> None:
        for listener in self.__listeners:
            listener(self)

    @abstractmethod
    def get_state(self) -> GraphicState:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def set_state(self, state: GraphicState) -> None:
        raise NotImplementedError("Subclasses must implement this method")