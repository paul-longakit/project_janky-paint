class DeleteLayerUseCase:

    def execute(
        self,
        paint,
        layer_index: int,
    ) -> None:
        paint.remove_layer(layer_index)