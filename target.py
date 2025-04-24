from multiprocessing import Process
from typing import Callable
from time import sleep
from cyberonics_py import Target


class LEDSequence(Target):

    def __init__(self, robot: 'PiBot'):
        self.robot = robot
        self.process = None
        super().__init__("LED Sequence", robot)


    def _run(self) -> Process:
        self.process = Process(target=self.__worker)
        self.process.start()
        return self.process

    async def _shutdown(self, beat: Callable[[], None]):
        if self.process:
            self.process.terminate()
            self.robot.blue_led.enabled.value = False
            self.robot.green_led.enabled.value = False

    def __worker(self):
        brightness = 0.25
        while True:
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

    def __simple_script(self):
        self.robot.blue_led.brightness.value = 0.5
        while True:
            print("set true")
            self.robot.blue_led.enabled.value = True
            sleep(3)
            print("set false")
            self.robot.blue_led.enabled.value = False
            sleep(3)
