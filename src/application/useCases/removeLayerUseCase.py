from domain.entities.paintAppEntity import JankyPaint


class RemoveLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        index: int,
    ) -> None:
        paint.remove_layer(index)