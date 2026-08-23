import tkinter as tk

from src.presentation.panels.colorPanel import ColorPanel
from src.presentation.views.canvas.canvasView import CanvasView
from src.presentation.views.layers.layerView import LayerView
from src.presentation.views.toolbar.toolbarView import ToolbarView
from src.presentation.views.topbar.topBarView import TopBarView


class EditorView:

    def __init__(
        self,
        root: tk.Tk,
        controller,
        layer_controller,
        on_undo,
        on_redo,
        on_color_change,
        on_layer_change,
        on_brush,
        on_eraser,
        on_bucket,
        on_brush_size_change,
    ):
        self._root = root
        self._controller = controller
        self._layer_controller = layer_controller

        # =========================================================
        # TOP BAR
        # =========================================================

        self._top_bar = TopBarView(
            parent=self._root,
            on_undo=on_undo,
            on_redo=on_redo,
        )

        self._top_bar.get_widget().pack(
            fill=tk.X,
        )

        # =========================================================
        # MAIN CONTENT
        # =========================================================

        self._main_frame = tk.Frame(
            self._root,
        )

        self._main_frame.pack(
            fill=tk.BOTH,
            expand=True,
        )

        # =========================================================
        # LEFT TOOLBAR
        # =========================================================

        self._toolbar_view = ToolbarView(
            parent=self._main_frame,
            current_brush_size=(
                self._controller.current_brush_size
            ),
            on_brush=on_brush,
            on_eraser=on_eraser,
            on_bucket=on_bucket,
            on_brush_size_change=(
                on_brush_size_change
            ),
        )

        self._toolbar_view.get_widget().pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=5,
            pady=5,
        )

        # =========================================================
        # COLOR PANEL
        # =========================================================

        self._color_panel = ColorPanel(
            parent=self._toolbar_view.get_widget(),
            initial_color=(
                self._controller.current_color
            ),
            on_color_change=on_color_change,
        )

        self._color_panel.pack(
            fill=tk.X,
            pady=10,
        )

        # =========================================================
        # CANVAS
        # =========================================================

        self._canvas_view = CanvasView(
            parent=self._main_frame,
        )

        self._canvas_view.get_widget().pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5,
        )

        # =========================================================
        # RIGHT LAYER PANEL
        # =========================================================

        self._layer_view = LayerView(
            parent=self._main_frame,
            layer_controller=self._layer_controller,
            on_layer_change=on_layer_change,
        )

        self._layer_view.get_widget().pack(
            side=tk.RIGHT,
            fill=tk.Y,
            padx=5,
            pady=5,
        )

        # =========================================================
        # INITIAL WINDOW SIZE
        # =========================================================

        self._root.update_idletasks()

        self._root.minsize(
            1000,
            700,
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def refresh_layers(self) -> None:

        self._layer_view.refresh()

    def refresh_canvas(self) -> None:

        image = self._controller.render()

        self._canvas_view.display_image(
            image
        )

    def set_history_state(
        self,
        can_undo: bool,
        can_redo: bool,
    ) -> None:

        self._top_bar.set_history_state(
            can_undo=can_undo,
            can_redo=can_redo,
        )

    # =========================================================
    # ACCESSORS
    # =========================================================

    @property
    def canvas_view(self) -> CanvasView:

        return self._canvas_view

    @property
    def layer_view(self) -> LayerView:

        return self._layer_view

    @property
    def top_bar(self) -> TopBarView:

        return self._top_bar