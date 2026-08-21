from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.value_objects.colorValueObject import Color
from src.domain.value_objects.pointValueObject import Point
from src.domain.abstractions.rendererAbstraction import Renderer


class FillAreaUseCase:

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def execute(
        self,
        paint: JankyPaintApp,
        point: Point,
        color: Color,
    ) -> None:

        operation = paint.fill_area(
            point=point,
            color=color,
        )

        self.renderer.render_operation(
            paint.active_layer,
            operation,
        )