from src.domain.entities.paintAppEntity import JankyPaintApp


class RenameLayerUseCase:
    def execute(
        self,
        paint: JankyPaintApp,
        index: int,
        name: str,
    ) -> None:
        if index < 0 or index >= len(paint.layers):
            raise IndexError("Layer index out of range.")

        paint.layers[index].rename(name)