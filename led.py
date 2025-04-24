from cyberonics_py import Device, DeviceProperty
from cyberonics_py.graphics import GraphicCell, Switch, Slider, HeaderText
import RPi.GPIO as GPIO


class LED(Device):
    def __init__(self, name: str, pin: int):
        self.pin = pin
        self.name = name

        self.brightness = DeviceProperty(float(0), True)
        self.enabled = DeviceProperty(False, True)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)

        self.graphic_cell = self.__make_graphic_cell()

        self.brightness.add_listener(self.__brightness_updated)
        self.enabled.add_listener(self.__enabled_updated)

        super().__init__([self.brightness, self.enabled], self.graphic_cell)

    def __set_brightness(self, duty_cycle: float):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def __brightness_updated(self, device_property: DeviceProperty):
        print("brightness updated. val: ", device_property.value)
        duty_cycle = device_property.value * 100
        if self.enabled.value:
            self.__set_brightness(duty_cycle)
        else:
            print("disabled")

    def __enabled_updated(self, device_property: DeviceProperty):
        print("enabled updated. val: ", device_property.value)
        if device_property.value:
            print("val yes")
            if self.brightness.value < 0.1:
                self.__set_brightness(0.5)
            self.__set_brightness(self.brightness.value * 100)
        else:
            print("val no")
            self.__set_brightness(0)

    def __make_graphic_cell(self) -> GraphicCell:
        header = HeaderText(self.name)
        switch = Switch(self.enabled)
        slider = Slider(self.brightness, float(0), float(1), float(0.1))
        return GraphicCell([header, switch, slider])


