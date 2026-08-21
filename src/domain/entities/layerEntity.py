from domain.entities.strokeEntity import Stroke
from domain.entities.fillEntity import FillOperation


class Layer:
    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Layer name cannot be empty.")

        self.name = name
        self.operations: list[Stroke | FillOperation] = []

    def add_operation(
        self,
        operation: Stroke | FillOperation,
    ) -> None:
        self.operations.append(operation)

    def remove_operation(self, index: int) -> None:
        if index < 0 or index >= len(self.operations):
            raise IndexError("Operation index out of range.")

        self.operations.pop(index)

    def clear(self) -> None:
        self.operations.clear()

    def rename(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Layer name cannot be empty.")

        self.name = name