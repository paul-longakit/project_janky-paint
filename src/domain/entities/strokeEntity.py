from src.domain.entities.paintingOperationEntity import PaintingOperation

from src.domain.value_objects.brushSettingsValueObject import BrushSettings
from src.domain.value_objects.pointValueObject import Point

from src.domain.enums.paintingOperationEnum import PaintingOperationType


class Stroke(PaintingOperation):
    def __init__(
        self,
        points: list[Point],
        settings: BrushSettings,
    ):
        super().__init__(
            PaintingOperationType.STROKE
        )

        if not points:
            raise ValueError(
                "A stroke must contain at least one point."
            )

        self.points = points
        self.settings = settings