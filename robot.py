from cyberonics_py import Robot

from led import LED
from target import LEDSequence


class PiBot(Robot):
    def __init__(self):
        self.green_led = LED("Green LED", 23)
        self.blue_led = LED("Blue LED", 24)
        self.target = LEDSequence(self)
        super().__init__([self.green_led, self.blue_led], [self.target])
