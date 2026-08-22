import tkinter as tk

from src.domain.value_objects.colorValueObject import Color


class ColorInfoView:

    def __init__(
        self,
        parent,
        on_hex_change,
    ):
        self._on_hex_change = on_hex_change

        self.frame = tk.Frame(
            parent,
        )

        # =====================================================
        # CURRENT COLOR
        # =====================================================

        tk.Label(
            self.frame,
            text="Current Color",
            anchor="w",
        ).pack(
            fill=tk.X,
        )

        self._color_preview = tk.Frame(
            self.frame,
            height=30,
            relief=tk.SUNKEN,
            bd=2,
        )

        self._color_preview.pack(
            fill=tk.X,
            pady=(2, 10),
        )

        self._color_preview.pack_propagate(
            False
        )

        # =====================================================
        # HSL
        # =====================================================

        tk.Label(
            self.frame,
            text="HSL",
            anchor="w",
        ).pack(
            fill=tk.X,
        )

        self._hsl_label = tk.Label(
            self.frame,
            text="H: 0   S: 0   L: 0",
            anchor="w",
        )

        self._hsl_label.pack(
            fill=tk.X,
        )

        # =====================================================
        # RGB
        # =====================================================

        tk.Label(
            self.frame,
            text="RGB",
            anchor="w",
        ).pack(
            fill=tk.X,
            pady=(5, 0),
        )

        self._rgb_label = tk.Label(
            self.frame,
            text="R: 0   G: 0   B: 0",
            anchor="w",
        )

        self._rgb_label.pack(
            fill=tk.X,
        )

        # =====================================================
        # HEX
        # =====================================================

        tk.Label(
            self.frame,
            text="HEX",
            anchor="w",
        ).pack(
            fill=tk.X,
            pady=(5, 0),
        )

        self._hex_variable = tk.StringVar(
            value="#000000"
        )

        self._hex_entry = tk.Entry(
            self.frame,
            textvariable=self._hex_variable,
        )

        self._hex_entry.pack(
            fill=tk.X,
        )

        self._hex_entry.bind(
            "<Return>",
            self._on_hex_submit,
        )

        self._hex_entry.bind(
            "<FocusOut>",
            self._on_hex_submit,
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def set_color(
        self,
        color: Color,
        hue: float,
        saturation: float,
        lightness: float,
    ) -> None:

        self._hsl_label.configure(
            text=(
                f"H: {round(hue * 360)}   "
                f"S: {round(saturation * 100)}   "
                f"L: {round(lightness * 100)}"
            )
        )

        self._rgb_label.configure(
            text=(
                f"R: {color.red}   "
                f"G: {color.green}   "
                f"B: {color.blue}"
            )
        )

        self._hex_variable.set(
            f"#{color.red:02X}"
            f"{color.green:02X}"
            f"{color.blue:02X}"
        )

        self._update_preview(
            color
        )

    def pack(self) -> None:

        self.frame.pack(
            fill=tk.X,
        )

    # =========================================================
    # PREVIEW
    # =========================================================

    def _update_preview(
        self,
        color: Color,
    ) -> None:

        hex_color = (
            f"#{color.red:02x}"
            f"{color.green:02x}"
            f"{color.blue:02x}"
        )

        self._color_preview.configure(
            bg=hex_color
        )

    # =========================================================
    # HEX
    # =========================================================

    def _on_hex_submit(
        self,
        _event=None,
    ) -> None:

        value = (
            self._hex_variable
            .get()
            .strip()
        )

        if not value.startswith("#"):
            value = "#" + value

        if len(value) != 7:
            return

        try:

            red = int(
                value[1:3],
                16,
            )

            green = int(
                value[3:5],
                16,
            )

            blue = int(
                value[5:7],
                16,
            )

        except ValueError:
            return

        self._on_hex_change(
            Color(
                red,
                green,
                blue,
            )
        )