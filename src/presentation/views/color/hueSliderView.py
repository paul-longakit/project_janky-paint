import colorsys
import tkinter as tk


class HueSliderView:

    WIDTH = 180
    HEIGHT = 20

    def __init__(
        self,
        parent,
        on_change,
    ):
        self._on_change = on_change

        self._hue = 0.0

        self.canvas = tk.Canvas(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            highlightthickness=1,
            highlightbackground="black",
            cursor="crosshair",
        )

        self.canvas.bind(
            "<Button-1>",
            self._on_mouse,
        )

        self.canvas.bind(
            "<B1-Motion>",
            self._on_mouse,
        )

        self._draw()

    # =========================================================
    # PUBLIC API
    # =========================================================

    def set_hue(
        self,
        hue: float,
    ) -> None:

        self._hue = max(
            0.0,
            min(1.0, hue),
        )

        self._draw()

    def pack(self) -> None:

        self.canvas.pack(
            pady=(0, 10),
        )

    # =========================================================
    # DRAWING
    # =========================================================

    def _draw(self) -> None:

        self.canvas.delete(
            "gradient"
        )

        width = self.WIDTH
        height = self.HEIGHT

        for x in range(width):

            hue = x / (width - 1)

            red, green, blue = colorsys.hsv_to_rgb(
                hue,
                1.0,
                1.0,
            )

            color = (
                f"#{round(red * 255):02x}"
                f"{round(green * 255):02x}"
                f"{round(blue * 255):02x}"
            )

            self.canvas.create_line(
                x,
                0,
                x,
                height,
                fill=color,
                tags="gradient",
            )

        selector_x = int(
            self._hue
            * (width - 1)
        )

        self.canvas.create_line(
            selector_x,
            0,
            selector_x,
            height,
            fill="white",
            width=2,
            tags="selector",
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _on_mouse(
        self,
        event,
    ) -> None:

        width = self.canvas.winfo_width()

        if width <= 1:
            return

        x = max(
            0,
            min(event.x, width - 1),
        )

        self._hue = (
            x / (width - 1)
        )

        self._draw()

        self._on_change(
            self._hue
        )