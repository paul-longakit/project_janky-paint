import tkinter as tk

from PIL import ImageTk


class CanvasView:

    def __init__(
        self,
        parent,
        width: int = 400,
        height: int = 400,
    ):
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="white",
            cursor="crosshair",
        )

        self.canvas.pack(
            padx=10,
            pady=10,
        )

        self.tk_image = None

    # =============================================================
    # EVENTS
    # =============================================================

    def bind(
        self,
        event: str,
        callback,
    ) -> None:
        self.canvas.bind(
            event,
            callback,
        )

    # =============================================================
    # RENDERING
    # =============================================================

    def display_image(self, image) -> None:

        self.tk_image = ImageTk.PhotoImage(
            image
        )

        self.canvas.delete("all")

        self.canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.tk_image,
        )

    # =============================================================
    # STROKE PREVIEW
    # =============================================================

    def draw_preview_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str,
        width: int,
    ) -> int:

        return self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
            smooth=True,
        )

    def remove_preview(
        self,
        preview_id: int,
    ) -> None:

        self.canvas.delete(
            preview_id
        )

    # =============================================================
    # ACCESS
    # =============================================================

    def get_widget(self):
        return self.canvas