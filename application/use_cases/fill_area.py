from domain.entities.janky_paint import JankyPaint
from domain.value_objects.color import Color
from domain.value_objects.point import Point


class FillAreaUseCase:

    def execute(
        self,
        paint: JankyPaint,
        point: Point,
        color: Color,
    ) -> None:
        paint.fill_area(
            point=point,
            color=color,
        )