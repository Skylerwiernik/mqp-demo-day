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
        self.robot.green_led.brightness.value = 0.5
        self.robot.blue_led.brightness.value = 0.5
        while self.running:
            self.__toggle_leds()
            sleep(2)


    def __toggle_leds(self):
        if self.robot.blue_led.enabled.value:
            if int(self.robot.green_led.brightness.value) == 1:
                self.robot.green_led.brightness.value = 0.25
            else:
                self.robot.green_led.brightness.value += 0.25

            self.robot.blue_led.enabled.value = False
            self.robot.green_led.enabled.value = True
        else:
            if int(self.robot.blue_led.brightness.value) == 1:
                self.robot.blue_led.brightness.value = 0.25
            else:
                self.robot.blue_led.brightness.value += 0.25

            self.robot.blue_led.enabled.value = True
            self.robot.green_led.enabled.value = False