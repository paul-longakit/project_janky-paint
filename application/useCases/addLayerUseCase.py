from domain.entities.paintAppEntity import JankyPaint
from domain.entities.layerEntity import Layer


class AddLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        name: str,
    ) -> None:
        layer = Layer(name)
        paint.add_layer(layer)