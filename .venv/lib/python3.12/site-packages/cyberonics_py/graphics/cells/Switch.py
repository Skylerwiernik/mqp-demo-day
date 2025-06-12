from ..Graphic import Graphic
from ..GraphicState import GraphicState
from ..GraphicTyping import Color
from ...DeviceProperty import DeviceProperty


class Switch(Graphic):
    def __init__(self, managed_property: DeviceProperty[bool], on_color=Color.SUCCESS, off_color=Color.DANGER) -> None:
        if not managed_property.mutable:
            raise ValueError("Managed property must be mutable")

        self.managed_property = managed_property
        managed_property.add_listener(lambda _: super(Switch, self)._notify())
        self.__on_color = on_color
        self.__off_color = off_color
        super().__init__(managed_property)
        super()._notify()

    @property
    def value(self) -> bool:
        return self.managed_property.value

    @value.setter
    def value(self, value: bool) -> None:
        self.managed_property.value = value

    @property
    def on_color(self) -> Color:
        return self.__on_color

    @on_color.setter
    def on_color(self, value: Color) -> None:
        self.__on_color = value
        super()._notify()

    @property
    def off_color(self) -> Color:
        return self.__off_color

    @off_color.setter
    def off_color(self, value: Color) -> None:
        self.__off_color = value
        super()._notify()

    def get_state(self) -> GraphicState:
        return GraphicState("Switch", super().uuid, value=self.value, on_color=self.on_color, off_color=self.off_color)

    def set_state(self, state: GraphicState) -> None:
        on: bool = getattr(state, "value", None)
        if on is None:
            raise ValueError("Invalid state data. Missing key 'value'")
        if not isinstance(on, bool):
            raise ValueError("Invalid state data. 'on' must be a boolean")
        self.managed_property.value = on
        super()._notify()