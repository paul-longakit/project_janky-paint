from domain.entities.layerEntity import Layer

class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.layers: list[Layer] = []
        self.active_layer_index = 0

    @property
    def active_layer(self) -> Layer:
        return self.layers[self.active_layer_index]

    def add_layer(self, layer: Layer):
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1

    def select_layer(self, index: int):
        if index < 0 or index >= len(self.layers):
            raise IndexError("Layer index out of range")

        self.active_layer_index = index

    def remove_layer(self, index: int):
        if index < 0 or index >= len(self.layers):
            raise IndexError("Layer index out of range")

        del self.layers[index]

        if self.active_layer_index >= len(self.layers):
            self.active_layer_index = len(self.layers) - 1