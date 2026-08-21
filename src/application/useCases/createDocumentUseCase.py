from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.entities.layerEntity import Layer

class CreateDocumentUseCase:

    def execute(
        self,
        width: int,
        height: int,
    ) -> JankyPaintApp:

        paint = JankyPaintApp(
            width=width,
            height=height,
        )

        paint.add_layer(
            Layer(
                layer_id=1,
                name="Layer 1",
                width=width,
                height=height,
            )
        )

        return paint