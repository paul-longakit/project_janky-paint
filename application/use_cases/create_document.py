from domain.entities.janky_paint import JankyPaint
from domain.entities.layer import Layer


class CreateDocumentUseCase:

    def execute(
        self,
        width: int,
        height: int,
    ) -> JankyPaint:

        paint = JankyPaint(
            width=width,
            height=height,
        )

        paint.add_layer(
            Layer("Layer 1")
        )

        return paint