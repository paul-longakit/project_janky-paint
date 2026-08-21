from domain.entities.paintAppEntity import JankyPaint
from domain.value_objects.colorValueObject import Color
from domain.value_objects.pointValueObject import Point


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