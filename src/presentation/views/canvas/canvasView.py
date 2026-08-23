import tkinter as tk

from PIL import ImageTk


class CanvasView:

    TRANSPARENCY_TILE_SIZE = 10
    TRANSPARENCY_LIGHT = "#ffffff"
    TRANSPARENCY_DARK = "#d9d9d9"

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
        # CANVAS PADDING
        # =========================================================

        self._canvas_container = tk.Frame(
            self._workspace,
            bg="#d0d0d0",
        )

        self._canvas_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=20,
        )

        # =========================================================
        # CANVAS
        # =========================================================

        self._canvas = tk.Canvas(
            self._canvas_container,
            width=width,
            height=height,
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

        # =========================================================
        # IMAGE
        # =========================================================

        self.tk_image = None

        # =========================================================
        # TRANSPARENCY BACKGROUND
        # =========================================================

        self._create_transparency_background()

    # =============================================================
    # TRANSPARENCY BACKGROUND
    # =============================================================

    def _create_transparency_background(
        self,
    ) -> None:

        tile_size = self.TRANSPARENCY_TILE_SIZE

        for row, y in enumerate(
            range(
                0,
                self._height,
                tile_size,
            )
        ):
            for column, x in enumerate(
                range(
                    0,
                    self._width,
                    tile_size,
                )
            ):

                color = (
                    self.TRANSPARENCY_LIGHT
                    if (row + column) % 2 == 0
                    else self.TRANSPARENCY_DARK
                )

                self._canvas.create_rectangle(
                    x,
                    y,
                    x + tile_size,
                    y + tile_size,
                    fill=color,
                    outline=color,
                    tags="transparency_background",
                )

        self._canvas.tag_lower(
            "transparency_background"
        )

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

        # Remove only the previous image.
        # Do NOT delete the transparency background.
        self._canvas.delete(
            "canvas_image"
        )

        self._canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.tk_image,
            tags="canvas_image",
        )

        # Make sure the image stays above
        # the transparency background.
        self._canvas.tag_raise(
            "canvas_image",
            "transparency_background",
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
            tags="stroke_preview",
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