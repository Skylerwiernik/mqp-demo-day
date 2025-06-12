import threading
from typing import Callable
from time import sleep
from cyberonics_py import Target


class LEDSequence(Target):

    def __init__(self, robot: 'PiBot'):
        self.robot = robot
        self.running = False
        self.thread = None
        super().__init__("LED Sequence", robot)


    def _run(self) -> threading.Thread:
        self.running = True
        self.thread = threading.Thread(target=self.__worker)
        self.thread.start()
        return self.thread

    async def _shutdown(self, beat: Callable[[], None]):
        if self.thread:
            self.running = False
            self.thread.join()

    def __worker(self):
        while self.running:
            if self.robot.led.enabled.value:
                print("Disabling")
                self.robot.led.value = False
            else:
                print("Enabling")
                self.robot.led.value = True
