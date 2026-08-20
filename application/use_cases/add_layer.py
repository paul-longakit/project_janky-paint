from domain.entities.janky_paint import JankyPaint
from domain.entities.layer import Layer


class AddLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        name: str,
    ) -> None:
        layer = Layer(name)
        paint.add_layer(layer)