from domain.entities.paintAppEntity import JankyPaint
from domain.entities.strokeEntity import Stroke
from domain.value_objects.brushSettingsValueObject import BrushSettings
from domain.value_objects.pointValueObject import Point


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

        paint.active_layer.add_operation(stroke)