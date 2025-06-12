from numbers import Number
from typing import TypeVar, Generic

from ..Graphic import Graphic
from ..GraphicState import GraphicState
from ..GraphicTyping import Color
from ...DeviceProperty import DeviceProperty

T = TypeVar("T", bound=Number)
class Slider(Graphic, Generic[T]):
    def __init__(self, managed_property: DeviceProperty[T], min_value: T, max_value: T, step: T = 1, color: Color = Color.PRIMARY) -> None:
        if not all([isinstance(x, Number) for x in (min_value, max_value, step)]):
            raise TypeError(f"min_val {min_value}, max_val {max_value}, step {step} must all be numeric types.")
        if not type(min_value) == type(max_value) == type(step):
            raise TypeError(f"min_val {min_value}, max_val {max_value}, step {step} must all be the same type.")
        if not managed_property.mutable:
            raise ValueError("Managed property must be mutable")

        self.managed_property: DeviceProperty[T] = managed_property
        managed_property.add_listener(lambda _: super(Slider, self)._notify())
        self.__min_value: T = min_value
        self.__max_value: T = max_value
        self.__step: T = step

        if min_value > max_value or self.managed_property.value < min_value or self.managed_property.value > max_value:
            raise ValueError("Invalid slider parameters")
        if step <= 0 or step > (max_value - min_value):
            raise ValueError("Invalid step value")
        self.__color = color
        super().__init__(managed_property)
        super()._notify()

    @property
    def value(self) -> T:
        return self.managed_property.value

    @value.setter
    def value(self, value: T) -> None:
        if self.__min_value > value or value > self.__max_value:
            raise ValueError("Attempted to set value out of bounds")
        self.managed_property.value = value

    @property
    def min_value(self) -> T:
        return self.__min_value

    @min_value.setter
    def min_value(self, min_value: T) -> None:
        self.__min_value = min_value
        super()._notify()

    @property
    def max_value(self) -> T:
        return self.__max_value

    @max_value.setter
    def max_value(self, max_value: T) -> None:
        self.__max_value = max_value
        super()._notify()

    @property
    def step(self) -> T:
        return self.__step

    @step.setter
    def step(self, step: T) -> None:
        self.__step = step
        super()._notify()

    @property
    def color(self) -> Color:
        return self.__color

    @color.setter
    def color(self, color: Color) -> None:
        self.__color = color
        super()._notify()

    def get_state(self) -> GraphicState:
        return GraphicState("Slider", super().uuid, value=self.value, min_value=self.min_value, max_value=self.max_value, step=self.step, color=self.color)

    def set_state(self, state: GraphicState) -> None:
        val: T = getattr(state, "value", None)
        if not isinstance(val, self.managed_property.type):
            try:
                val = self.managed_property.type(val)
            except:
                raise ValueError(f"Invalid state data. Did not find {T} value for 'value'")
        self.value = val
