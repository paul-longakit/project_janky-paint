from src.domain.entities.paintAppEntity import JankyPaintApp


class ClearLayerUseCase:
    def execute(
        self,
        paint: JankyPaintApp,
    ) -> None:
        paint.active_layer.clear()