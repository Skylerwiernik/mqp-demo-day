from ..Graphic import Graphic
from ..GraphicState import GraphicState
from ..GraphicTyping import Color, Alignment
from ...DeviceProperty import DeviceProperty


class StatusDot(Graphic):
    def __init__(self, color: DeviceProperty[Color], alignment: Alignment = Alignment.LEFT) -> None:
        if color.type != Color:
            raise ValueError("color must be of type Color")
        self.__color = color
        color.add_listener(lambda _: super(StatusDot, self)._notify())
        self.__flash = False
        self.__alignment = alignment
        super().__init__(None)
        super()._notify()

    def flash(self):
        self.__flash = True
        super()._notify()
        self.__flash = False

    @property
    def color(self) -> Color:
        return self.__color.value

    @color.setter
    def color(self, value: Color) -> None:
        self.__color.value = value
        super()._notify()


    def get_state(self) -> GraphicState:
        return GraphicState("StatusDot", super().uuid, color=self.__color.value, flash=self.__flash, alignment=self.__alignment)

    def set_state(self, state: GraphicState) -> None:
        if self.get_state() != state:
            raise ValueError("StatusDot cannot by set by the client")