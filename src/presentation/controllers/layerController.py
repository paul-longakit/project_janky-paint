from src.application.useCases.renameLayerUseCase import RenameLayerUseCase

class LayerController:

    def __init__(
        self,
        editor_controller,
    ):
        self.editor_controller = editor_controller
        self.rename_layer_use_case = RenameLayerUseCase()

    # =============================================================
    # LAYER ACTIONS
    # =============================================================

    def add_layer(self) -> None:

        layer_number = len(
            self.editor_controller.paint.layers
        ) + 1

        self.editor_controller.add_layer(
            f"Layer {layer_number}"
        )

    def delete_layer(self) -> None:

        paint = self.editor_controller.paint

        if len(paint.layers) <= 1:
            return

        if paint.active_layer_index is None:
            return

        self.editor_controller.delete_layer(
            paint.active_layer_index
        )

    def select_layer(
        self,
        index: int,
    ) -> None:

        self.editor_controller.select_layer(
            index
        )

    def reorder_layer(
        self,
        from_index: int,
        to_index: int,
    ) -> None:

        self.editor_controller.reorder_layer(
            from_index=from_index,
            to_index=to_index,
        )

    def rename_layer(
        self,
        index: int,
        name: str,
    ) -> None:

        self.editor_controller.rename_layer(
            index=index,
            name=name,
        )
    # =============================================================
    # ACCESS
    # =============================================================

    def get_layers(self):
        return self.editor_controller.paint.layers

    def get_active_layer_index(self):
        return self.editor_controller.paint.active_layer_index