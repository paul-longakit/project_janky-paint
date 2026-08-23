import tkinter as tk

from src.presentation.views.layers.layerItemView import LayerItemView
from src.presentation.controllers.layerDragController import LayerDragController


class LayerView:

    def __init__(
        self,
        parent,
        layer_controller,
        on_layer_change=None,
    ):
        self.layer_controller = layer_controller
        self.on_layer_change = on_layer_change

        self.frame = tk.Frame(
            parent,
            relief=tk.RAISED,
            bd=2,
        )

        self.layer_items = []

        # =========================================================
        # DRAG CONTROLLER
        # =========================================================

        self.drag_controller = LayerDragController(
            layer_list=None,
            get_layer_items=lambda: self.layer_items,
            get_layers=self.layer_controller.get_layers,
            reorder_layer=self.layer_controller.reorder_layer,
            on_reorder_complete=self._on_reorder_complete,
        )

        # =========================================================
        # BUILD
        # =========================================================

        self._build_header()
        self._build_layer_list()
        self._build_controls()

        self.drag_controller.layer_list = self.layer_list

        self.refresh()

    # =============================================================
    # HEADER
    # =============================================================

    def _build_header(self) -> None:

        tk.Label(
            self.frame,
            text="Layers",
            font=("Arial", 10, "bold"),
        ).pack(
            fill=tk.X,
            padx=5,
            pady=(5, 2),
        )

    # =============================================================
    # LAYER LIST
    # =============================================================

    def _build_layer_list(self) -> None:

        self.layer_list = tk.Frame(
            self.frame,
        )

        self.layer_list.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5,
        )

    # =============================================================
    # CONTROLS
    # =============================================================

    def _build_controls(self) -> None:

        controls = tk.Frame(
            self.frame,
        )

        controls.pack(
            fill=tk.X,
            padx=5,
            pady=(0, 5),
        )

        tk.Button(
            controls,
            text="+",
            command=self._add_layer,
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=1,
        )

        tk.Button(
            controls,
            text="-",
            command=self._delete_layer,
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=1,
        )

    # =============================================================
    # LAYER ACTIONS
    # =============================================================

    def _add_layer(self) -> None:

        self.layer_controller.add_layer()

        self.refresh()

        self._notify_layer_change()

    def _delete_layer(self) -> None:

        self.layer_controller.delete_layer()

        self.refresh()

        self._notify_layer_change()

    def _select_layer(
        self,
        index: int,
    ) -> None:

        self.layer_controller.select_layer(
            index
        )

        self.refresh()

        self._notify_layer_change()

    # =============================================================
    # MOUSE DOWN
    # =============================================================

    def _on_mouse_down(
        self,
        index: int,
        event,
    ) -> None:

        if self.drag_controller.mouse_down:
            return

        # ---------------------------------------------------------
        # SELECT LAYER
        # ---------------------------------------------------------

        self.layer_controller.select_layer(
            index
        )

        # Update selection visually without refresh.
        for item_index, item in enumerate(
            self.layer_items
        ):

            item.frame.configure(
                relief=(
                    tk.SUNKEN
                    if item_index == index
                    else tk.RAISED
                )
            )

        # ---------------------------------------------------------
        # START DRAG
        # ---------------------------------------------------------

        self.drag_controller.on_mouse_down(
            index,
            event,
        )

        self._notify_layer_change()

    # =============================================================
    # MOUSE MOVE
    # =============================================================

    def _on_mouse_move(
        self,
        index: int,
        event,
    ) -> None:

        self.drag_controller.on_mouse_move(
            index,
            event,
        )

    # =============================================================
    # MOUSE UP
    # =============================================================

    def _on_mouse_up(
        self,
        index: int,
        event,
    ) -> None:

        self.drag_controller.on_mouse_up(
            index,
            event,
        )

    # =============================================================
    # REORDER CALLBACK
    # =============================================================

    def _on_reorder_complete(self) -> None:

        self.refresh()

        self._notify_layer_change()

    # =============================================================
    # REFRESH
    # =============================================================

    def refresh(self) -> None:

        self.drag_controller.reset()

        for item in self.layer_items:
            item.destroy()

        self.layer_items = []

        layers = (
            self.layer_controller
            .get_layers()
        )

        active_index = (
            self.layer_controller
            .get_active_layer_index()
        )

        for index, layer in enumerate(
            layers
        ):

            item = LayerItemView(
                parent=self.layer_list,
                index=index,
                name=layer.name,
                active=(
                    index == active_index
                ),
                on_mouse_down=self._on_mouse_down,
                on_mouse_move=self._on_mouse_move,
                on_mouse_up=self._on_mouse_up,
                on_rename=self._rename_layer,
            )

            item.pack()

            self.layer_items.append(
                item
            )

    # =============================================================
    # RENAME
    # =============================================================

    def _rename_layer(
        self,
        index: int,
        name: str,
    ) -> None:

        try:

            self.layer_controller.rename_layer(
                index=index,
                name=name,
            )

        except ValueError:
            return

        self.refresh()

        self._notify_layer_change()

    # =============================================================
    # DISPLAY
    # =============================================================

    def pack(self) -> None:

        self.frame.pack(
            side=tk.RIGHT,
            fill=tk.Y,
            padx=5,
            pady=5,
        )

    # =============================================================
    # CALLBACK
    # =============================================================

    def _notify_layer_change(self) -> None:

        if self.on_layer_change:
            self.on_layer_change()

    # =============================================================
    # WIDGET
    # =============================================================

    def get_widget(self) -> tk.Frame:

        return self.frame