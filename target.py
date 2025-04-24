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
            self.robot.blue_led.enabled.value = False
            self.robot.green_led.enabled.value = False

    def __worker(self):
        brightness = 0.25
        while self.running:
            self.robot.blue_led.brightness.value = brightness
            self.robot.blue_led.enabled.value = True
            sleep(3)
            self.robot.blue_led.enabled.value = False
            self.robot.green_led.brightness.value = brightness
            self.robot.green_led.enabled.value = True
            sleep(3)
            self.robot.green_led.enabled.value = False
            if brightness == 1:
                brightness = 0
            else:
                brightness += 0.25
