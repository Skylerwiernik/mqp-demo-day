import json
from enum import Enum
from uuid import UUID, uuid4



class GraphicState:
    def __init__(self, graphic_type: str, uuid: uuid4, **kwargs):
        self.type = graphic_type
        self.uuid = uuid
        self.__dict__.update(kwargs)

    def encode(self):
        state_dict = self.__dict__.copy()
        state_dict['uuid'] = str(self.uuid)
        return json.dumps(state_dict)

    @staticmethod
    def decode(state: dict[str, any]) -> 'GraphicState':
        graphic_type = state.pop('type')
        uuid_obj = UUID(state.pop('uuid'))
        return GraphicState(graphic_type, uuid_obj, **state)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        def normalize(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, str):
                return value.replace(" ", "").strip().lower()
            return value

        self_dict = {key: normalize(value) for key, value in self.__dict__.items()}
        other_dict = {key: normalize(value) for key, value in other.__dict__.items()}
        return str(self_dict).lower() == str(other_dict).lower()