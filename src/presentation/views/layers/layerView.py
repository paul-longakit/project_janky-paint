import tkinter as tk

from src.presentation.views.layers.layerItemView import LayerItemView


class LayerView:

    DRAG_THRESHOLD = 5

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
        # DRAG STATE
        # =========================================================

        self.mouse_down = False
        self.dragging = False

        self.dragged_index = None

        self.start_x = 0
        self.start_y = 0

        self.drop_index = None

        self.drag_preview = None
        self.drop_indicator = None

        # =========================================================
        # BUILD
        # =========================================================

        self._build_header()
        self._build_layer_list()
        self._build_controls()

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

        if self.mouse_down:
            return

        # ---------------------------------------------------------
        # SELECT LAYER
        # ---------------------------------------------------------
        #
        # IMPORTANT:
        # Do NOT call _select_layer() here because _select_layer()
        # calls refresh(), and refresh() resets the drag state.
        #

        self.layer_controller.select_layer(
            index
        )

        # Update the visual selection without rebuilding the
        # LayerItemViews.
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
        # START DRAG STATE
        # ---------------------------------------------------------

        self.mouse_down = True
        self.dragging = False

        self.dragged_index = index

        self.start_x = event.x_root
        self.start_y = event.y_root

        self.drop_index = index

        self._notify_layer_change()

    # =============================================================
    # MOUSE MOVE
    # =============================================================

    def _on_mouse_move(
        self,
        index: int,
        event,
    ) -> None:

        if not self.mouse_down:
            return

        if self.dragged_index != index:
            return

        delta_x = abs(
            event.x_root - self.start_x
        )

        delta_y = abs(
            event.y_root - self.start_y
        )

        # ---------------------------------------------------------
        # START DRAG
        # ---------------------------------------------------------

        if not self.dragging:

            if (
                delta_x < self.DRAG_THRESHOLD
                and delta_y < self.DRAG_THRESHOLD
            ):
                return

            self.dragging = True

            dragged_index = self.dragged_index

            if dragged_index is None:
                return

            self._create_drag_preview(
                dragged_index,
                event,
            )

        # ---------------------------------------------------------
        # MOVE PREVIEW
        # ---------------------------------------------------------

        self._move_drag_preview(
            event
        )

        # ---------------------------------------------------------
        # DROP SLOT
        # ---------------------------------------------------------

        target_index = self._get_drop_index(
            event
        )

        if target_index is None:
            return

        if target_index != self.drop_index:

            self.drop_index = target_index

            self._update_drop_indicator()

    # =============================================================
    # MOUSE UP
    # =============================================================

    def _on_mouse_up(
        self,
        index: int,
        event,
    ) -> None:

        if not self.mouse_down:
            return

        if self.dragging:

            self._finish_drag(
                self.dragged_index,
                self.drop_index,
            )

        self._reset_drag_state()

    # =============================================================
    # FINISH DRAG
    # =============================================================

    def _finish_drag(
        self,
        from_index,
        to_index,
    ) -> None:

        self._destroy_drag_preview()
        self._destroy_drop_indicator()

        if from_index is None:
            return

        if to_index is None:
            return

        layers = self.layer_controller.get_layers()

        if not layers:
            return

        # ---------------------------------------------------------
        # CONVERT DROP SLOT TO FINAL INDEX
        # ---------------------------------------------------------

        final_index = to_index

        if to_index > from_index:
            final_index -= 1

        final_index = max(
            0,
            min(
                final_index,
                len(layers) - 1,
            ),
        )

        if from_index == final_index:
            return

        self.layer_controller.reorder_layer(
            from_index=from_index,
            to_index=final_index,
        )

        self.refresh()

        self._notify_layer_change()

    # =============================================================
    # RESET
    # =============================================================

    def _reset_drag_state(self) -> None:

        self.mouse_down = False
        self.dragging = False

        self.dragged_index = None
        self.drop_index = None

        self.start_x = 0
        self.start_y = 0

        self._destroy_drag_preview()
        self._destroy_drop_indicator()

    # =============================================================
    # DROP TARGET
    # =============================================================

    def _get_drop_index(
        self,
        event,
    ):
        if not self.layer_items:
            return None

        mouse_y = (
            event.y_root
            - self.layer_list.winfo_rooty()
        )

        for index, item in enumerate(
            self.layer_items
        ):

            item.frame.update_idletasks()

            top = item.frame.winfo_y()
            height = item.frame.winfo_height()

            middle = top + (
                height / 2
            )

            if mouse_y < middle:
                return index

        return len(
            self.layer_items
        )

    # =============================================================
    # DROP INDICATOR
    # =============================================================

    def _update_drop_indicator(self) -> None:

        self._destroy_drop_indicator()

        if self.drop_index is None:
            return

        if not self.layer_items:
            return

        if self.drop_index == 0:

            target = self.layer_items[0]

            target.frame.update_idletasks()

            y = target.frame.winfo_y()

        elif self.drop_index >= len(
            self.layer_items
        ):

            target = self.layer_items[-1]

            target.frame.update_idletasks()

            y = (
                target.frame.winfo_y()
                + target.frame.winfo_height()
            )

        else:

            target = self.layer_items[
                self.drop_index
            ]

            target.frame.update_idletasks()

            y = target.frame.winfo_y()

        self.drop_indicator = tk.Frame(
            self.layer_list,
            height=3,
            bg="black",
        )

        self.drop_indicator.place(
            x=0,
            y=y,
            relwidth=1,
        )

        self.drop_indicator.lift()

    def _destroy_drop_indicator(self) -> None:

        if self.drop_indicator is not None:

            self.drop_indicator.destroy()

            self.drop_indicator = None

    # =============================================================
    # DRAG PREVIEW
    # =============================================================

    def _create_drag_preview(
        self,
        index: int,
        event,
    ) -> None:

        if index < 0:
            return

        if index >= len(
            self.layer_items
        ):
            return

        item = self.layer_items[
            index
        ]

        self.drag_preview = tk.Toplevel(
            self.frame
        )

        self.drag_preview.overrideredirect(
            True
        )

        self.drag_preview.attributes(
            "-alpha",
            0.75,
        )

        label = tk.Label(
            self.drag_preview,
            text=item.label.cget("text"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=4,
        )

        label.pack()

        self._move_drag_preview(
            event
        )

    def _move_drag_preview(
        self,
        event,
    ) -> None:

        if self.drag_preview is None:
            return

        x = event.x_root + 10
        y = event.y_root + 10

        self.drag_preview.geometry(
            f"+{x}+{y}"
        )

    def _destroy_drag_preview(self) -> None:

        if self.drag_preview is not None:

            self.drag_preview.destroy()

            self.drag_preview = None

    # =============================================================
    # REFRESH
    # =============================================================

    def refresh(self) -> None:

        self._reset_drag_state()

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
            )

            item.pack()

            self.layer_items.append(
                item
            )

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