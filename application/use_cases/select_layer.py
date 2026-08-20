from domain.entities.janky_paint import JankyPaint


class SelectLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        index: int,
    ) -> None:
        paint.select_layer(index)