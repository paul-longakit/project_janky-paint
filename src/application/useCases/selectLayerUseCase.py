from src.domain.entities.paintAppEntity import JankyPaintApp

class SelectLayerUseCase:

    def execute(
        self,
        paint,
        layer_index: int,
    ) -> None:
        paint.select_layer(layer_index)