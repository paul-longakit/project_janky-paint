from domain.value_objects.color import Color
from domain.value_objects.point import Point
from domain.entities.layer import Layer
from domain.entities.fill import FillOperation

class JankyPaint:
    def __init__(self, width: int, height: int):
        if width <= 0:
            raise ValueError("Canvas width must be greater than zero.")

        if height <= 0:
            raise ValueError("Canvas height must be greater than zero.")

        self.width = width
        self.height = height

        self.layers: list[Layer] = []
        self.active_layer_index: int | None = None

    @property
    def active_layer(self) -> Layer:
        if self.active_layer_index is None:
            raise RuntimeError("No active layer exists.")

        return self.layers[self.active_layer_index]

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1

    def select_layer(self, index: int) -> None:
        if index < 0 or index >= len(self.layers):
            raise IndexError("Layer index out of range.")

        self.active_layer_index = index

    def remove_layer(self, index: int) -> None:
        if index < 0 or index >= len(self.layers):
            raise IndexError("Layer index out of range.")

        self.layers.pop(index)

        if not self.layers:
            self.active_layer_index = None
            return

        if self.active_layer_index is not None:
            self.active_layer_index = min(
                self.active_layer_index,
                len(self.layers) - 1,
            )
    def fill_area(
        self,
        point: Point,
        color: Color,
    ) -> None:
        operation = FillOperation(
            point=point,
            color=color,
        )

        self.active_layer.add_operation(operation)