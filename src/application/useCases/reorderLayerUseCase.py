class ReorderLayerUseCase:

    def execute(
        self,
        paint,
        from_index: int,
        to_index: int,
    ) -> None:

        layers = paint.layers

        if from_index < 0:
            return

        if from_index >= len(layers):
            return

        if to_index < 0:
            return

        if to_index >= len(layers):
            return

        if from_index == to_index:
            return

        layer = layers.pop(from_index)

        layers.insert(
            to_index,
            layer,
        )

        # Keep the moved layer active.
        paint.active_layer_index = to_index