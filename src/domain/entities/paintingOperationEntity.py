from abc import ABC

from src.domain.enums.paintingOperationEnum import PaintingOperationType


class PaintingOperation(ABC):

    def __init__(
        self,
        operation_type: PaintingOperationType,
    ):
        self.operation_type = operation_type