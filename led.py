from cyberonics_py import Device, DeviceProperty
from cyberonics_py.graphics import GraphicCell, Switch, Slider, HeaderText
#import RPi.GPIO as GPIO


class LED(Device):
    def __init__(self, name: str):
        self.name = name
        self.enabled = DeviceProperty(False, True)

        self.graphic_cell = self.__make_graphic_cell()
        self.enabled.add_listener(self.__enabled_updated)

        super().__init__([self.enabled], self.graphic_cell)


    def __enabled_updated(self, prop: DeviceProperty):
        if prop.value:
            print("Enabled!")
        else:
            print("Disabled!")


    def __make_graphic_cell(self) -> GraphicCell:
        header = HeaderText(self.name)
        switch = Switch(self.enabled)
        return GraphicCell([header, switch])


