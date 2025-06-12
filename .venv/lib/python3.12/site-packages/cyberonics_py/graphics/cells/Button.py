from collections.abc import Callable

from ..Graphic import Graphic
from ..GraphicState import GraphicState
from ..GraphicTyping import Color


class Button(Graphic):
    def __init__(self, text: str, onclick: Callable, text_color: Color = Color.PRIMARY, background_color: Color = Color.BACKGROUND) -> None:
        self.__text = text
        self.__on_click = onclick
        self.__text_color = text_color
        self.__background_color = background_color
        super().__init__(None)
        super()._notify()

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        self.__text = value
        super()._notify()

    @property
    def text_color(self) -> Color:
        return self.__text_color

    @text_color.setter
    def text_color(self, value: Color) -> None:
        self.__text_color = value
        super()._notify()

    @property
    def background_color(self) -> Color:
        return self.__background_color

    @background_color.setter
    def background_color(self, value: Color) -> None:
        self.__background_color = value
        super()._notify()

    def get_state(self) -> GraphicState:
        return GraphicState("Button", super().uuid, pressed=False, text=self.text, text_color=self.text_color, background_color=self.background_color)

    def set_state(self, state: GraphicState) -> None:
        pressed: bool = getattr(state, "pressed", None)
        if not isinstance(pressed, bool):
            raise ValueError("Invalid state data. Did not find boolean value for 'pressed'")
        if pressed:
            self.__on_click()
