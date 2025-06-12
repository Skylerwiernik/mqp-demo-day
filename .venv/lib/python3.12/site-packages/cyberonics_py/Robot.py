from abc import ABC
from typing import Optional
from .Device import Device
from .Target import Target


class Robot(ABC):
    def __init__(self, devices: Optional[list[Device]], targets: Optional[list[Target]] = None):
        self.__devices = devices or []
        self.__targets = {t.name: t for t in targets or []}
        self.__active_target: Optional[Target] = None

    @property
    def devices(self) -> list[Device]:
        return self.__devices

    @property
    def targets(self) -> list[Target]:
        return self.__targets.values()

    def run_target(self, name: str):
        target = self.__targets.get(name)
        if not target:
            raise Exception(f"Target {name} not found")
        self.__active_target = target
        target.run()

    @property
    def is_running(self) -> bool:
        return self.__active_target is not None

    def stop_execution(self):
        self.__active_target.shutdown()
        self.__active_target = None