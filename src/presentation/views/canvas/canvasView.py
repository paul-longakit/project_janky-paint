import tkinter as tk

from PIL import ImageTk


class CanvasView:

    def __init__(
        self,
        parent,
        width: int = 400,
        height: int = 400,
    ):
        self._width = width
        self._height = height

        # =========================================================
        # WORKSPACE
        # =========================================================

        self._workspace = tk.Frame(
            parent,
            bg="#d0d0d0",
        )

        self._workspace.pack_propagate(
            False
        )

        # =========================================================
        # CANVAS
        # =========================================================

        self._canvas = tk.Canvas(
            self._workspace,
            width=width,
            height=height,
            bg="white",
            highlightthickness=1,
            highlightbackground="black",
            cursor="crosshair",
        )

        self._canvas.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER,
            width=width,
            height=height,
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

        self._canvas.bind(
            event,
            callback,
        )

    # =============================================================
    # RENDERING
    # =============================================================

    def display_image(
        self,
        image,
    ) -> None:

        self.tk_image = ImageTk.PhotoImage(
            image
        )

        self._canvas.delete(
            "all"
        )

        self._canvas.create_image(
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

        return self._canvas.create_line(
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

        self._canvas.delete(
            preview_id
        )

    # =============================================================
    # WIDGET
    # =============================================================

    def get_widget(
        self,
    ) -> tk.Frame:

        return self._workspace

    # =============================================================
    # CANVAS
    # =============================================================

    def get_canvas(
        self,
    ) -> tk.Canvas:

        return self._canvas