import tkinter as tk

from src.domain.value_objects.colorValueObject import Color

from src.presentation.presenters.color.colorPickerPresenter import (
    ColorPickerPresenter,
)

from src.presentation.state.colorPickerState import (
    ColorPickerState,
)

from src.presentation.views.color.colorFieldView import (
    ColorFieldView,
)

from src.presentation.views.color.hueSliderView import (
    HueSliderView,
)

from src.presentation.views.color.colorInfoView import (
    ColorInfoView,
)


class ColorPanel(tk.LabelFrame):

    def __init__(
        self,
        parent: tk.Widget,
        initial_color: Color,
        on_color_change,
        **kwargs,
    ):
        super().__init__(
            parent,
            text="COLOR",
            padx=5,
            pady=5,
            **kwargs,
        )

        self._on_color_change = (
            on_color_change
        )

        # =====================================================
        # STATE
        # =====================================================

        self._state = ColorPickerState()

        # =====================================================
        # PRESENTER
        # =====================================================

        self._presenter = ColorPickerPresenter(
            state=self._state,
        )

        # =====================================================
        # COMPONENTS
        # =====================================================

        self._color_field = ColorFieldView(
            self,
            on_change=self._on_field_change,
        )

        self._hue_slider = HueSliderView(
            self,
            on_change=self._on_hue_change,
        )

        self._color_info = ColorInfoView(
            self,
            on_hex_change=self._on_hex_change,
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        self._color_field.pack()

        tk.Label(
            self,
            text="Hue",
            anchor="w",
        ).pack(
            fill=tk.X,
        )

        self._hue_slider.pack()

        self._color_info.pack()

        # =====================================================
        # INITIAL COLOR
        # =====================================================

        self.sync_from_color(
            initial_color
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def sync_from_color(
        self,
        color: Color,
    ) -> None:

        self._presenter.sync_from_color(
            color
        )

        self._sync_views(
            color
        )

    # =========================================================
    # VIEW SYNCHRONIZATION
    # =========================================================

    def _sync_views(
        self,
        color: Color,
    ) -> None:

        self._hue_slider.set_hue(
            self._state.hue
        )

        self._color_field.set_hue(
            self._state.hue
        )

        self._color_field.set_selection(
            self._state.saturation,
            self._state.lightness,
        )

        self._color_info.set_color(
            color=color,
            hue=self._state.hue,
            saturation=self._state.saturation,
            lightness=self._state.lightness,
        )

    # =========================================================
    # FIELD
    # =========================================================

    def _on_field_change(
        self,
        saturation: float,
        lightness: float,
    ) -> None:

        color = self._presenter.update_field(
            saturation,
            lightness,
        )

        self._color_info.set_color(
            color=color,
            hue=self._state.hue,
            saturation=self._state.saturation,
            lightness=self._state.lightness,
        )

        self._on_color_change(
            color
        )

    # =========================================================
    # HUE
    # =========================================================

    def _on_hue_change(
        self,
        hue: float,
    ) -> None:

        color = self._presenter.update_hue(
            hue
        )

        self._color_field.set_hue(
            hue
        )

        self._color_info.set_color(
            color=color,
            hue=self._state.hue,
            saturation=self._state.saturation,
            lightness=self._state.lightness,
        )

        self._on_color_change(
            color
        )

    # =========================================================
    # HEX
    # =========================================================

    def _on_hex_change(
        self,
        color: Color,
    ) -> None:

        self.sync_from_color(
            color
        )

        self._on_color_change(
            color
        )