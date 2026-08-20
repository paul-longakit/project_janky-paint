from domain.entities.janky_paint import JankyPaint


class RemoveLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        index: int,
    ) -> None:
        paint.remove_layer(index)