from domain.value_objects.brush_settings import BrushSettings
from domain.value_objects.point import Point


class Stroke:
    def __init__(
        self,
        points: list[Point],
        settings: BrushSettings,
    ):
        if not points:
            raise ValueError(
                "A stroke must contain at least one point."
            )

        self.points = points
        self.settings = settings