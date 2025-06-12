from cyberonics_py import Robot

from led import LED
from target import LEDSequence


class PiBot(Robot):
    def __init__(self):
        self.led = LED("Green LED")
        self.target = LEDSequence(self)
        super().__init__([self.led], [self.target])
