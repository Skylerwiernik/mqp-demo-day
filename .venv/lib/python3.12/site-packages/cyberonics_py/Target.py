from abc import ABC, abstractmethod
from typing import Callable, TYPE_CHECKING, final
from multiprocessing import Process
import asyncio
import time

if TYPE_CHECKING:
    from .Robot import Robot


class Target(ABC):

    def __init__(self, name: str, robot: 'Robot', shutdown_timeout: float = 0.5):
        self._name = name
        self.robot = robot
        self.shutdown_timeout = shutdown_timeout
        self.__worker_process = None

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def _run(self) -> Process:
        pass

    @final
    def run(self):
        self.__worker_process = self._run()


    @abstractmethod
    async def _shutdown(self, beat: Callable[[], None]):
        pass

    @final
    def shutdown(self):
        if self.__worker_process is None:
            return

        async def shutdown_task():
            shutdown_complete = asyncio.Event()
            last_heartbeat = time.monotonic()

            def beat():
                nonlocal last_heartbeat
                last_heartbeat = time.monotonic()

            async def monitor_shutdown():
                while not shutdown_complete.is_set():
                    await asyncio.sleep(0.1)
                    if time.monotonic() - last_heartbeat > self.shutdown_timeout:
                        if self.__worker_process.is_alive():
                            print(f"[WARNING] Worker process '{self._name}' did not shut down in time. Terminating.")
                            self.__worker_process.terminate()
                            self.__worker_process.join()
                        shutdown_complete.set()

            monitor_task = asyncio.create_task(monitor_shutdown())
            await self._shutdown(beat)
            shutdown_complete.set()
            await monitor_task
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(shutdown_task())
            else:
                loop.run_until_complete(shutdown_task())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(shutdown_task())