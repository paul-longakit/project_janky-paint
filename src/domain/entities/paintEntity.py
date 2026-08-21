from src.domain.entities.layerEntity import Layer


class Paint:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.layers: list[Layer] = []
        self.active_layer_index = 0

    def add_layer(self, name: str) -> Layer:

        layer = Layer(
            layer_id=len(self.layers) + 1,
            name=name,
            width=self.width,
            height=self.height,
        )

        self.layers.append(layer)

        self.active_layer_index = len(self.layers) - 1

        return layer

    def remove_layer(self, index: int) -> None:

        if len(self.layers) <= 1:
            return

        if index < 0 or index >= len(self.layers):
            return

        self.layers.pop(index)

        if self.active_layer_index >= len(self.layers):
            self.active_layer_index = len(self.layers) - 1

    def select_layer(self, index: int) -> None:

        if index < 0 or index >= len(self.layers):
            return

        self.active_layer_index = index

    @property
    def active_layer(self) -> Layer:
        return self.layers[self.active_layer_index]