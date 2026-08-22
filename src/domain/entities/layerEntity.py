from PIL import Image


class Layer:

    def __init__(
        self,
        layer_id: int,
        name: str,
        width: int,
        height: int,
    ):
        self.id = layer_id
        self.name = name

        self.image = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0),
        )

        self.visible = True
        self.opacity = 255

        self.operations = []

    def add_operation(self, operation) -> None:
        self.operations.append(operation)

    def clear(self) -> None:
        self.operations.clear()

    def rename(self, name: str) -> None:

        name = name.strip()

        if not name:
            raise ValueError(
                "Layer name cannot be empty."
            )

        self.name = name

    def set_visibility(self, visible: bool) -> None:
        self.visible = visible

    def set_opacity(self, opacity: int) -> None:
        self.opacity = max(0, min(255, opacity))