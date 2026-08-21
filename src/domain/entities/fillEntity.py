from src.domain.entities.paintingOperationEntity import PaintingOperation

from src.domain.value_objects.colorValueObject import Color
from src.domain.value_objects.pointValueObject import Point

from src.domain.enums.paintingOperationEnum import PaintingOperationType


class FillOperation(PaintingOperation):
    def __init__(
        self,
        point: Point,
        color: Color,
    ):
        super().__init__(
            PaintingOperationType.FILL
        )
        self.point = point
        self.color = color