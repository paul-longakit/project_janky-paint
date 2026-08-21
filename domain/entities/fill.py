from domain.value_objects.color import Color
from domain.value_objects.point import Point


class FillOperation:
    def __init__(
        self,
        point: Point,
        color: Color,
    ):
        self.point = point
        self.color = color