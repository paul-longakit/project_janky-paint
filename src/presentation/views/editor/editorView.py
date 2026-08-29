import tkinter as tk

from src.presentation.panels.colorPanel import ColorPanel
from src.presentation.views.canvas.canvasView import CanvasView
from src.presentation.views.layers.layerView import LayerView
from src.presentation.views.toolbar.toolbarView import ToolbarView
from src.presentation.views.topbar.topBarView import TopBarView


class EditorView:

    LEFT_PANEL_WIDTH = 180
    RIGHT_PANEL_WIDTH = 180

    CANVAS_MIN_WIDTH = 440

    CANVAS_AREA_BG = "#d0d0d0"

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
        on_eyedropper,
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

        self._main_frame = tk.PanedWindow(
            self._root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=4,
            opaqueresize=False,
        )

        # Temporary visual indicator used while dragging a sash.
        #
        # A Canvas is used instead of a Frame so we can use
        # stipple to create a subtle transparent-looking effect.
        self._sash_indicator = tk.Canvas(
            self._root,
            width=6,
            highlightthickness=0,
            bd=0,
            bg=self.CANVAS_AREA_BG,
        )

        self._sash_indicator.create_rectangle(
            0,
            0,
            6,
            1,
            fill="#666666",
            outline="",
            stipple="gray50",
            tags="sash_indicator",
        )

        self._sash_indicator.place_forget()

        self._sash_dragging = False

        # No additional root-level bindings are required.

        self._main_frame.bind(
            "<ButtonPress-1>",
            self._on_sash_press,
        )

        self._main_frame.bind(
            "<B1-Motion>",
            self._on_sash_drag,
        )

        self._main_frame.bind(
            "<ButtonRelease-1>",
            self._on_sash_release,
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
            on_eyedropper=on_eyedropper,
            on_brush_size_change=(
                on_brush_size_change
            ),
        )

        self._main_frame.add(
            self._toolbar_view.get_widget(),
            minsize=self.LEFT_PANEL_WIDTH,
            width=self.LEFT_PANEL_WIDTH,
            stretch="never",
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
            fill=tk.BOTH,
            expand=True,
            pady=10,
        )

        # =========================================================
        # CANVAS AREA
        # =========================================================

        self._canvas_area = tk.Frame(
            self._main_frame,
            bg=self.CANVAS_AREA_BG,
        )

        self._main_frame.add(
            self._canvas_area,
            minsize=self.CANVAS_MIN_WIDTH,
            stretch="always",
        )

        # ---------------------------------------------------------
        # CANVAS
        # ---------------------------------------------------------

        self._canvas_view = CanvasView(
            parent=self._canvas_area,
        )

        self._canvas_view.get_widget().pack(
            fill=tk.BOTH,
            expand=True,
        )

        # =========================================================
        # RIGHT LAYER PANEL
        # =========================================================

        self._layer_view = LayerView(
            parent=self._main_frame,
            layer_controller=self._layer_controller,
            on_layer_change=on_layer_change,
        )

        self._main_frame.add(
            self._layer_view.get_widget(),
            minsize=self.RIGHT_PANEL_WIDTH,
            width=self.RIGHT_PANEL_WIDTH,
            stretch="never",
        )

        # =========================================================
        # INITIAL WINDOW SIZE
        # =========================================================

        self._root.minsize(
            1000,
            700,
        )

        self._root.update_idletasks()

        # =========================================================
        # INITIAL PANE POSITIONS
        # =========================================================
        #
        # Force the canvas to receive most of the available space.
        # The side panels start at fixed widths.
        #

        window_width = self._main_frame.winfo_width()

        left_sash = self.LEFT_PANEL_WIDTH

        right_sash = (
            window_width
            - self.RIGHT_PANEL_WIDTH
        )

        self._main_frame.sash_place(
            0,
            left_sash,
            0,
        )

        self._main_frame.sash_place(
            1,
            right_sash,
            0,
        )

    # =============================================================
    # SASH DRAG INDICATOR
    # =============================================================

    def _on_sash_press(
        self,
        event,
    ) -> None:

        sash_index = self._get_sash_at(
            event.x,
            event.y,
        )

        if sash_index is None:
            return

        self._sash_dragging = True

        self._show_sash_indicator(
            event.x,
        )


    def _on_sash_drag(
        self,
        event,
    ) -> None:

        if not self._sash_dragging:
            return

        # Convert root coordinates back into PanedWindow coordinates.
        main_x = (
            event.x_root
            - self._main_frame.winfo_rootx()
        )

        self._show_sash_indicator(
            main_x,
        )


    def _on_sash_release(
        self,
        event,
    ) -> None:

        if not self._sash_dragging:
            return

        self._sash_dragging = False

        self._sash_indicator.place_forget()

        self._root.update_idletasks()

    def _show_sash_indicator(
        self,
        x: int,
    ) -> None:

        root_x = (
            self._main_frame.winfo_rootx()
            - self._root.winfo_rootx()
            + x
        )

        root_y = (
            self._main_frame.winfo_rooty()
            - self._root.winfo_rooty()
        )

        height = self._main_frame.winfo_height()

        self._sash_indicator.delete(
            "sash_indicator"
        )

        self._sash_indicator.create_rectangle(
            0,
            0,
            6,
            height,
            fill="#666666",
            outline="",
            stipple="gray50",
            tags="sash_indicator",
        )

        self._sash_indicator.place(
            x=root_x - 3,
            y=root_y,
            width=6,
            height=height,
        )

        self._sash_indicator.place(
            x=root_x - 3,
            y=root_y,
            width=6,
            height=height,
        )

    def _get_sash_at(
        self,
        x: int,
        y: int,
    ):
        for index in range(
            self._main_frame.panes().__len__() - 1
        ):

            try:

                sash_x, sash_y = (
                    self._main_frame.sash_coord(
                        index
                    )
                )

            except tk.TclError:
                continue

            if (
                abs(x - sash_x) <= 6
                and abs(y - sash_y) <= 8
            ):
                return index

        return None

    # =============================================================
    # PUBLIC API
    # =============================================================

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

    # =============================================================
    # ACCESSORS
    # =============================================================

    @property
    def canvas_view(self) -> CanvasView:

        return self._canvas_view

    @property
    def layer_view(self) -> LayerView:

        return self._layer_view

    @property
    def top_bar(self) -> TopBarView:

        return self._top_bar