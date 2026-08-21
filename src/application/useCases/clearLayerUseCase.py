from domain.entities.paintAppEntity import JankyPaint


class ClearLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
    ) -> None:
        paint.active_layer.clear()