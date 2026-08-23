import colorsys

from src.domain.value_objects.colorValueObject import Color

from src.presentation.state.colorPickerState import (
    ColorPickerState,
)


class ColorPickerPresenter:

    def __init__(
        self,
        state: ColorPickerState,
    ):
        self._state = state

    # =========================================================
    # STATE
    # =========================================================

    @property
    def state(self) -> ColorPickerState:
        return self._state

    # =========================================================
    # COLOR → STATE
    # =========================================================

    def sync_from_color(
        self,
        color: Color,
    ) -> None:

        red = color.red
        green = color.green
        blue = color.blue

        hue, lightness, saturation = (
            colorsys.rgb_to_hls(
                red / 255,
                green / 255,
                blue / 255,
            )
        )

        # -----------------------------------------------------
        # Achromatic colors have no meaningful hue.
        #
        # Preserve the existing hue when saturation is zero.
        # -----------------------------------------------------

        if saturation > 0:
            self._state.hue = hue

        self._state.saturation = saturation
        self._state.lightness = lightness

    # =========================================================
    # STATE → COLOR
    # =========================================================

    def color_from_state(self) -> Color:

        red, green, blue = (
            colorsys.hls_to_rgb(
                self._state.hue,
                self._state.lightness,
                self._state.saturation,
            )
        )

        return Color(
            round(red * 255),
            round(green * 255),
            round(blue * 255),
        )

    # =========================================================
    # UPDATE SATURATION / LIGHTNESS
    # =========================================================

    def update_field(
        self,
        saturation: float,
        lightness: float,
    ) -> Color:

        self._state.saturation = saturation
        self._state.lightness = lightness

        return self.color_from_state()

    # =========================================================
    # UPDATE HUE
    # =========================================================

    def update_hue(
        self,
        hue: float,
    ) -> Color:

        self._state.hue = hue

        return self.color_from_state()