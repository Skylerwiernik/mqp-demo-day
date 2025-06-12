from enum import Enum

class Alignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class Color(str, Enum):
    PRIMARY = "#61DAFB"
    SECONDARY = "#6c757d"
    LIGHT = "#f8f9fa"
    BACKGROUND = "#2a2a2c"
    SUCCESS = "#28a745"
    DANGER = "#dc3545"
    WARNING = "#ffc107"

    @staticmethod
    def hex(color_code: str):
        if not (color_code.startswith("#") and len(color_code) == 7):
            raise ValueError("Custom color must be a valid hex code, e.g., '#123abc'")
        return color_code

    @staticmethod
    def rgb(red: int, green: int, blue: int) -> str:
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("RGB values must be in the range 0-255.")
        return f"#{red:02x}{green:02x}{blue:02x}"