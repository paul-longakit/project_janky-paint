from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.entities.strokeEntity import Stroke
from src.domain.value_objects.brushSettingsValueObject import BrushSettings
from src.domain.value_objects.pointValueObject import Point
from src.domain.abstractions.rendererAbstraction import Renderer


class DrawStrokeUseCase:

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def execute(
        self,
        paint: JankyPaintApp,
        points: list[Point],
        settings: BrushSettings,
    ) -> None:

        stroke = Stroke(
            points=points,
            settings=settings,
        )

        paint.active_layer.add_operation(stroke)

        self.renderer.render_operation(
            paint.active_layer,
            stroke,
        )