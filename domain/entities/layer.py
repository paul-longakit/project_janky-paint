from domain.entities.stroke import Stroke

class Layer:
    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Layer name cannot be empty.")

        self.name = name
        self.strokes: list[Stroke] = []

    def add_stroke(self, stroke: Stroke) -> None:
        self.strokes.append(stroke)

    def remove_stroke(self, index: int) -> None:
        if index < 0 or index >= len(self.strokes):
            raise IndexError("Stroke index out of range.")

        self.strokes.pop(index)

    def clear(self) -> None:
        self.strokes.clear()

    def rename(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Layer name cannot be empty.")

        self.name = name