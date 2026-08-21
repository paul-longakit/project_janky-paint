from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.entities.layerEntity import Layer


class AddLayerUseCase:

    def execute(
        self,
        paint: JankyPaintApp,
        name: str,
    ) -> None:

        layer_id = len(paint.layers) + 1

        layer = Layer(
            layer_id=layer_id,
            name=name,
            width=paint.width,
            height=paint.height,
        )

        paint.add_layer(layer)