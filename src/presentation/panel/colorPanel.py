import tkinter as tk
import colorsys

from PIL import Image, ImageTk

from src.domain.value_objects.colorValueObject import Color


class ColorPanel(tk.LabelFrame):
    """
    A self-contained HSL color-picker panel.

    Wraps the hue slider, saturation/lightness field, color preview
    swatch, and HSL / RGB / HEX readouts into a single tk.LabelFrame
    widget.  Callers supply an ``on_color_change`` callback that is
    invoked whenever the user selects a new colour.
    """

    # =========================================================
    # CONSTANTS
    # =========================================================

    _FIELD_WIDTH = 180
    _FIELD_HEIGHT = 150

    _HUE_WIDTH = 180
    _HUE_HEIGHT = 20

    # =========================================================
    # CONSTRUCTION
    # =========================================================

    def __init__(
        self,
        parent: tk.Widget,
        initial_color: Color,
        on_color_change,
        **kwargs,
    ):
        super().__init__(parent, text="COLOR", padx=5, pady=5, **kwargs)

        self._on_color_change = on_color_change

        # Internal HSL state
        self._current_hue = 0.0
        self._current_saturation = 1.0
        self._current_lightness = 0.5

        # PIL image references (prevent GC)
        self._color_field_image = None
        self._color_field_image_tk = None
        self._color_field_image_id = None
        self._color_selector_id = None

        self._build_color_field()
        self._build_hue_slider()
        self._build_current_color()
        self._build_hsl_labels()
        self._build_rgb_labels()
        self._build_hex_entry()

        # Kick off initial draw
        self._draw_hue_slider()
        self._draw_color_field()
        self.sync_from_color(initial_color)

    # =========================================================
    # PUBLIC API
    # =========================================================

    def sync_from_color(self, color: Color) -> None:
        """Update all controls to reflect *color* without firing the callback."""
        red, green, blue = color.red, color.green, color.blue

        h, l, s = colorsys.rgb_to_hls(
            red / 255,
            green / 255,
            blue / 255,
        )

        self._current_hue = h
        self._current_saturation = s
        self._current_lightness = l

        self._hsl_label.configure(
            text=(
                f"H: {round(h * 360)}   "
                f"S: {round(s * 100)}   "
                f"L: {round(l * 100)}"
            )
        )

        self._rgb_label.configure(
            text=(
                f"R: {red}   "
                f"G: {green}   "
                f"B: {blue}"
            )
        )

        self._hex_variable.set(
            f"#{red:02X}{green:02X}{blue:02X}"
        )

        self._update_color_preview(color)
        self._draw_hue_slider()
        self._update_color_field_selector()

    # =========================================================
    # WIDGET CONSTRUCTION (private)
    # =========================================================

    def _build_color_field(self) -> None:
        self._color_field = tk.Canvas(
            self,
            width=self._FIELD_WIDTH,
            height=self._FIELD_HEIGHT,
            highlightthickness=1,
            highlightbackground="black",
            cursor="crosshair",
        )

        self._color_field.pack(pady=(0, 8))

        self._color_field.bind("<Button-1>", self._on_field_click)
        self._color_field.bind("<B1-Motion>", self._on_field_click)

    def _build_hue_slider(self) -> None:
        tk.Label(self, text="Hue", anchor="w").pack(fill=tk.X)

        self._hue_canvas = tk.Canvas(
            self,
            width=self._HUE_WIDTH,
            height=self._HUE_HEIGHT,
            highlightthickness=1,
            highlightbackground="black",
            cursor="crosshair",
        )

        self._hue_canvas.pack(pady=(0, 10))

        self._hue_canvas.bind("<Button-1>", self._on_hue_click)
        self._hue_canvas.bind("<B1-Motion>", self._on_hue_click)

    def _build_current_color(self) -> None:
        tk.Label(self, text="Current Color", anchor="w").pack(fill=tk.X)

        self._color_preview = tk.Frame(
            self,
            height=30,
            relief=tk.SUNKEN,
            bd=2,
        )

        self._color_preview.pack(fill=tk.X, pady=(2, 10))
        self._color_preview.pack_propagate(False)

    def _build_hsl_labels(self) -> None:
        tk.Label(self, text="HSL", anchor="w").pack(fill=tk.X)

        self._hsl_label = tk.Label(
            self,
            text="H: 0   S: 0   L: 0",
            anchor="w",
        )

        self._hsl_label.pack(fill=tk.X)

    def _build_rgb_labels(self) -> None:
        tk.Label(self, text="RGB", anchor="w").pack(fill=tk.X, pady=(5, 0))

        self._rgb_label = tk.Label(
            self,
            text="R: 0   G: 0   B: 0",
            anchor="w",
        )

        self._rgb_label.pack(fill=tk.X)

    def _build_hex_entry(self) -> None:
        tk.Label(self, text="HEX", anchor="w").pack(fill=tk.X, pady=(5, 0))

        self._hex_variable = tk.StringVar(value="#000000")

        self._hex_entry = tk.Entry(self, textvariable=self._hex_variable)
        self._hex_entry.pack(fill=tk.X)

        self._hex_entry.bind("<Return>", self._on_hex_submit)
        self._hex_entry.bind("<FocusOut>", self._on_hex_submit)

    # =========================================================
    # DRAWING
    # =========================================================

    def _draw_hue_slider(self) -> None:
        self._hue_canvas.delete("all")

        width = self._HUE_WIDTH
        height = self._HUE_HEIGHT

        for x in range(width):
            hue = x / width

            red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            color = (
                f"#{round(red * 255):02x}"
                f"{round(green * 255):02x}"
                f"{round(blue * 255):02x}"
            )

            self._hue_canvas.create_line(x, 0, x, height, fill=color)

        selector_x = int(self._current_hue * width)

        self._hue_canvas.create_line(
            selector_x,
            0,
            selector_x,
            height,
            fill="white",
            width=2,
        )

    def _draw_color_field(self) -> None:
        width = self._FIELD_WIDTH
        height = self._FIELD_HEIGHT

        image = Image.new("RGB", (width, height))

        for x in range(width):
            saturation = x / (width - 1)

            for y in range(height):
                lightness = 1.0 - (y / (height - 1))

                red, green, blue = colorsys.hls_to_rgb(
                    self._current_hue,
                    lightness,
                    saturation,
                )

                image.putpixel(
                    (x, y),
                    (
                        round(red * 255),
                        round(green * 255),
                        round(blue * 255),
                    ),
                )

        self._color_field_image = image
        self._color_field_image_tk = ImageTk.PhotoImage(image)

        if self._color_field_image_id is None:
            self._color_field_image_id = self._color_field.create_image(
                0, 0, anchor=tk.NW, image=self._color_field_image_tk
            )
        else:
            self._color_field.itemconfigure(
                self._color_field_image_id,
                image=self._color_field_image_tk,
            )

        self._update_color_field_selector()

    def _update_color_field_selector(self) -> None:
        width = self._FIELD_WIDTH
        height = self._FIELD_HEIGHT

        selector_x = int(self._current_saturation * (width - 1))
        selector_y = int((1.0 - self._current_lightness) * (height - 1))

        if self._color_selector_id is None:
            self._color_selector_id = self._color_field.create_oval(
                selector_x - 5,
                selector_y - 5,
                selector_x + 5,
                selector_y + 5,
                outline="white",
                width=2,
            )
        else:
            self._color_field.coords(
                self._color_selector_id,
                selector_x - 5,
                selector_y - 5,
                selector_x + 5,
                selector_y + 5,
            )

        self._color_field.tag_raise(self._color_selector_id)

    def _update_color_preview(self, color: Color) -> None:
        hex_color = (
            f"#{color.red:02x}"
            f"{color.green:02x}"
            f"{color.blue:02x}"
        )

        self._color_preview.configure(bg=hex_color)

    # =========================================================
    # EVENT HANDLERS
    # =========================================================

    def _on_field_click(self, event) -> None:
        width = self._color_field.winfo_width()
        height = self._color_field.winfo_height()

        if width <= 0 or height <= 0:
            return

        x = max(0, min(event.x, width - 1))
        y = max(0, min(event.y, height - 1))

        self._current_saturation = x / (width - 1)
        self._current_lightness = 1.0 - (y / (height - 1))

        self._update_color_field_selector()
        self._emit_hsl_color()

    def _on_hue_click(self, event) -> None:
        width = self._hue_canvas.winfo_width()

        if width <= 0:
            return

        x = max(0, min(event.x, width - 1))

        self._current_hue = x / (width - 1)

        self._draw_color_field()
        self._emit_hsl_color()

    def _on_hex_submit(self, _event=None) -> None:
        value = self._hex_variable.get().strip()

        if not value.startswith("#"):
            value = "#" + value

        if len(value) != 7:
            return

        try:
            red = int(value[1:3], 16)
            green = int(value[3:5], 16)
            blue = int(value[5:7], 16)
        except ValueError:
            return

        color = Color(red, green, blue)

        self._on_color_change(color)
        self.sync_from_color(color)

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _emit_hsl_color(self) -> None:
        red, green, blue = colorsys.hls_to_rgb(
            self._current_hue,
            self._current_lightness,
            self._current_saturation,
        )

        color = Color(
            round(red * 255),
            round(green * 255),
            round(blue * 255),
        )

        self._on_color_change(color)
        self.sync_from_color(color)
