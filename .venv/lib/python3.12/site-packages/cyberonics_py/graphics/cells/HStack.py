from ..GraphicTyping import Alignment
from ..Graphic import Graphic
from ..GraphicState import GraphicState


class HStack(Graphic):
    def __init__(self, graphics: list[Graphic], alignment: Alignment = Alignment.LEFT, space_between = 5) -> None:
        self.graphics = {graphic.uuid: graphic for graphic in graphics}
        self.__alignment = alignment
        self.__space_between = space_between
        super().__init__(None)

    @property
    def alignment(self) -> str:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: str) -> None:
        self.__alignment = value
        super()._notify()

    @property
    def space_between(self) -> int:
        return self.__space_between

    @space_between.setter
    def space_between(self, value: int) -> None:
        self.__space_between = value
        super()._notify()

    def get_state(self) -> GraphicState:
        graphics = [graphic.get_state().encode() for graphic in self.graphics.values()]
        return GraphicState("HStack", super().uuid, graphics=graphics)

    def set_state(self, state: GraphicState) -> None:
        graphics: [GraphicState] = getattr(state, "graphics", None)
        if graphics is None:
            raise ValueError("Invalid state")
        for graphic_state in graphics:
            if graphic_state.uuid not in self.graphics:
                raise ValueError("Invalid state")
            self.graphics[graphic_state.uuid].set_state(graphic_state)
