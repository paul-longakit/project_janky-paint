from dataclasses import dataclass


@dataclass
class ColorPickerState:
    hue: float = 0.0
    saturation: float = 1.0
    lightness: float = 0.5