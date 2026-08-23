import colorsys
import tkinter as tk

from PIL import Image, ImageTk


class ColorFieldView:

    WIDTH = 180
    HEIGHT = 150

    def __init__(
        self,
        parent: tk.Widget,
        on_change,
    ):
        self._on_change = on_change

        self._hue = 0.0
        self._saturation = 1.0
        self._lightness = 0.5

        self._image_tk = None
        self._image_id = None
        self._selector_id = None

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

        self._hue = self._clamp(
            hue
        )

        self._draw()

    def set_selection(
        self,
        saturation: float,
        lightness: float,
    ) -> None:

        self._saturation = self._clamp(
            saturation
        )

        self._lightness = self._clamp(
            lightness
        )

        self._update_selector()

    def pack(self) -> None:

        self.canvas.pack(
            pady=(0, 8),
        )

    # =========================================================
    # DRAWING
    # =========================================================

    def _draw(self) -> None:

        image = self._create_color_image()

        self._image_tk = ImageTk.PhotoImage(
            image
        )

        if self._image_id is None:

            self._image_id = (
                self.canvas.create_image(
                    0,
                    0,
                    anchor=tk.NW,
                    image=self._image_tk,
                )
            )

        else:

            self.canvas.itemconfigure(
                self._image_id,
                image=self._image_tk,
            )

        self._update_selector()

    def _create_color_image(
        self,
    ) -> Image.Image:

        image = Image.new(
            "RGB",
            (
                self.WIDTH,
                self.HEIGHT,
            ),
        )

        for x in range(self.WIDTH):

            saturation = (
                x / (self.WIDTH - 1)
            )

            for y in range(self.HEIGHT):

                lightness = (
                    1.0
                    - (
                        y
                        / (self.HEIGHT - 1)
                    )
                )

                red, green, blue = (
                    colorsys.hls_to_rgb(
                        self._hue,
                        lightness,
                        saturation,
                    )
                )

                image.putpixel(
                    (x, y),
                    (
                        round(red * 255),
                        round(green * 255),
                        round(blue * 255),
                    ),
                )

        return image

    def _update_selector(self) -> None:

        x = int(
            self._saturation
            * (self.WIDTH - 1)
        )

        y = int(
            (1.0 - self._lightness)
            * (self.HEIGHT - 1)
        )

        if self._selector_id is None:

            self._selector_id = (
                self.canvas.create_oval(
                    x - 5,
                    y - 5,
                    x + 5,
                    y + 5,
                    outline="white",
                    width=2,
                )
            )

        else:

            self.canvas.coords(
                self._selector_id,
                x - 5,
                y - 5,
                x + 5,
                y + 5,
            )

        self.canvas.tag_raise(
            self._selector_id
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _on_mouse(
        self,
        event,
    ) -> None:

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        x = max(
            0,
            min(
                event.x,
                width - 1,
            ),
        )

        y = max(
            0,
            min(
                event.y,
                height - 1,
            ),
        )

        self._saturation = (
            x / (width - 1)
        )

        self._lightness = (
            1.0
            - (
                y / (height - 1)
            )
        )

        self._update_selector()

        self._on_change(
            self._saturation,
            self._lightness,
        )

    # =========================================================
    # UTILITIES
    # =========================================================

    @staticmethod
    def _clamp(
        value: float,
    ) -> float:

        return max(
            0.0,
            min(
                1.0,
                value,
            ),
        )