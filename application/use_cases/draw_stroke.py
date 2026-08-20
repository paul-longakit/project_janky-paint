from domain.entities.janky_paint import JankyPaint
from domain.entities.stroke import Stroke
from domain.value_objects.brush_settings import BrushSettings
from domain.value_objects.point import Point


class DrawStrokeUseCase:
    def execute(
        self,
        paint: JankyPaint,
        points: list[Point],
        settings: BrushSettings,
    ) -> None:

        stroke = Stroke(
            points=points,
            settings=settings,
        )

        paint.active_layer.add_stroke(stroke)