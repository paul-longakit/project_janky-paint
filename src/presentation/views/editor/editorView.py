import tkinter as tk

from src.presentation.panel.colorPanel import ColorPanel
from src.presentation.views.layers.layerView import LayerView


class EditorView:

    def __init__(
        self,
        root: tk.Tk,
        controller,
        layer_controller,
        toolbar,
        on_color_change,
        on_layer_change,
    ):
        self.root = root
        self.controller = controller
        self.layer_controller = layer_controller
        self.toolbar = toolbar

        # =========================================================
        # COLOR PANEL
        # =========================================================

        self._build_color_panel(
            on_color_change=on_color_change,
        )

        # =========================================================
        # LAYER PANEL
        # =========================================================

        self._build_layer_panel(
            on_layer_change=on_layer_change,
        )

    # =============================================================
    # COLOR PANEL
    # =============================================================

    def _build_color_panel(
        self,
        on_color_change,
    ) -> None:

        self.color_panel = ColorPanel(
            parent=self.toolbar,
            initial_color=self.controller.current_color,
            on_color_change=on_color_change,
        )

        self.color_panel.pack(
            fill=tk.X,
            pady=10,
        )

    # =============================================================
    # LAYER PANEL
    # =============================================================

    def _build_layer_panel(
        self,
        on_layer_change,
    ) -> None:

        self.layer_view = LayerView(
            parent=self.root,
            layer_controller=self.layer_controller,
            on_layer_change=on_layer_change,
        )

        self.layer_view.pack()