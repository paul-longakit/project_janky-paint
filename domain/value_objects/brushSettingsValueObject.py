from dataclasses import dataclass

from domain.value_objects.colorValueObject import Color
from domain.enums.paintToolEnum import PaintTool


@dataclass(frozen=True)
class BrushSettings:
    color: Color
    size: int
    tool: PaintTool = PaintTool.BRUSH

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError(
                "Brush size must be greater than zero."
            )