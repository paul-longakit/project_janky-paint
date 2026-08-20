from domain.entities.janky_paint import JankyPaint


class RenameLayerUseCase:
    def execute(
        self,
        paint: JankyPaint,
        index: int,
        name: str,
    ) -> None:
        if index < 0 or index >= len(paint.layers):
            raise IndexError("Layer index out of range.")

        paint.layers[index].rename(name)