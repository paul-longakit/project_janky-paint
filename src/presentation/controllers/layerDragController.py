from typing import Callable, Optional
import tkinter as tk


class LayerDragController:

    DRAG_THRESHOLD = 5

    def __init__(
        self,
        layer_list: Optional[tk.Frame],
        get_layer_items: Callable,
        get_layers: Callable,
        reorder_layer: Callable,
        on_reorder_complete: Optional[Callable] = None,
    ):
        self.layer_list = layer_list
        self.get_layer_items = get_layer_items
        self.get_layers = get_layers
        self.reorder_layer = reorder_layer
        self.on_reorder_complete = on_reorder_complete

        self.mouse_down: bool = False
        self.dragging: bool = False

        self.dragged_index: Optional[int] = None

        self.start_x: int = 0
        self.start_y: int = 0

        self.drop_index: Optional[int] = None

        self.drag_preview: Optional[tk.Toplevel] = None
        self.drop_indicator: Optional[tk.Frame] = None

    # =============================================================
    # MOUSE DOWN
    # =============================================================

    def on_mouse_down(
        self,
        index: int,
        event,
    ) -> None:

        if self.mouse_down:
            return

        self.mouse_down = True
        self.dragging = False

        self.dragged_index = index

        self.start_x = event.x_root
        self.start_y = event.y_root

        self.drop_index = index

    # =============================================================
    # MOUSE MOVE
    # =============================================================

    def on_mouse_move(
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

            self.create_drag_preview(
                dragged_index,
                event,
            )

        # ---------------------------------------------------------
        # MOVE PREVIEW
        # ---------------------------------------------------------

        self.move_drag_preview(event)

        # ---------------------------------------------------------
        # DROP SLOT
        # ---------------------------------------------------------

        target_index = self.get_drop_index(event)

        if target_index is None:
            return

        if target_index != self.drop_index:

            self.drop_index = target_index

            self.update_drop_indicator()

    # =============================================================
    # MOUSE UP
    # =============================================================

    def on_mouse_up(
        self,
        index: int,
        event,
    ) -> None:

        if not self.mouse_down:
            return

        if self.dragging:

            self.finish_drag(
                self.dragged_index,
                self.drop_index,
            )

        self.reset()

    # =============================================================
    # FINISH DRAG
    # =============================================================

    def finish_drag(
        self,
        from_index: Optional[int],
        to_index: Optional[int],
    ) -> None:

        self.destroy_drag_preview()
        self.destroy_drop_indicator()

        if from_index is None:
            return

        if to_index is None:
            return

        layers = self.get_layers()

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

        self.reorder_layer(
            from_index=from_index,
            to_index=final_index,
        )

        if self.on_reorder_complete:
            self.on_reorder_complete()

    # =============================================================
    # DROP TARGET
    # =============================================================

    def get_drop_index(
        self,
        event,
    ):

        layer_items = self.get_layer_items()

        if not layer_items:
            return None

        if self.layer_list is None:
            return None

        mouse_y = (
            event.y_root
            - self.layer_list.winfo_rooty()
        )

        for index, item in enumerate(
            layer_items
        ):

            item.frame.update_idletasks()

            top = item.frame.winfo_y()
            height = item.frame.winfo_height()

            middle = top + (
                height / 2
            )

            if mouse_y < middle:
                return index

        return len(layer_items)

    # =============================================================
    # DROP INDICATOR
    # =============================================================

    def update_drop_indicator(self) -> None:

        self.destroy_drop_indicator()

        if self.drop_index is None:
            return

        layer_items = self.get_layer_items()

        if not layer_items:
            return

        if self.layer_list is None:
            return

        if self.drop_index == 0:

            target = layer_items[0]

            target.frame.update_idletasks()

            y = target.frame.winfo_y()

        elif self.drop_index >= len(
            layer_items
        ):

            target = layer_items[-1]

            target.frame.update_idletasks()

            y = (
                target.frame.winfo_y()
                + target.frame.winfo_height()
            )

        else:

            target = layer_items[
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

    def destroy_drop_indicator(self) -> None:

        if self.drop_indicator is not None:

            self.drop_indicator.destroy()

            self.drop_indicator = None

    # =============================================================
    # DRAG PREVIEW
    # =============================================================

    def create_drag_preview(
        self,
        index: int,
        event,
    ) -> None:

        layer_items = self.get_layer_items()

        if index < 0:
            return

        if index >= len(layer_items):
            return

        if self.layer_list is None:
            return

        item = layer_items[index]

        self.drag_preview = tk.Toplevel(
            self.layer_list
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

        self.move_drag_preview(event)

    def move_drag_preview(
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

    def destroy_drag_preview(self) -> None:

        if self.drag_preview is not None:

            self.drag_preview.destroy()

            self.drag_preview = None

    # =============================================================
    # RESET
    # =============================================================

    def reset(self) -> None:

        self.mouse_down = False
        self.dragging = False

        self.dragged_index = None
        self.drop_index = None

        self.start_x = 0
        self.start_y = 0

        self.destroy_drag_preview()
        self.destroy_drop_indicator()