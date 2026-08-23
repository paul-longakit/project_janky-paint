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
        # SCROLL CONTAINER
        # =====================================================

        self._scroll_container = tk.Frame(
            self,
        )

        self._scroll_container.pack(
            fill=tk.BOTH,
            expand=True,
        )

        self._scroll_canvas = tk.Canvas(
            self._scroll_container,
            highlightthickness=0,
            borderwidth=0,
        )

        self._scrollbar = tk.Scrollbar(
            self._scroll_container,
            orient=tk.VERTICAL,
            command=self._scroll_canvas.yview,
        )

        self._scroll_canvas.configure(
            yscrollcommand=self._scrollbar.set,
        )

        self._scroll_canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        self._content_frame = tk.Frame(
            self._scroll_canvas,
        )

        self._canvas_window = (
            self._scroll_canvas.create_window(
                0,
                0,
                window=self._content_frame,
                anchor=tk.NW,
            )
        )

        # =====================================================
        # COMPONENTS
        # =====================================================

        self._color_field = ColorFieldView(
            self._content_frame,
            on_change=self._on_field_change,
        )

        self._hue_slider = HueSliderView(
            self._content_frame,
            on_change=self._on_hue_change,
        )

        self._color_info = ColorInfoView(
            self._content_frame,
            on_hex_change=self._on_hex_change,
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        self._color_field.pack()

        tk.Label(
            self._content_frame,
            text="Hue",
            anchor="w",
        ).pack(
            fill=tk.X,
        )

        self._hue_slider.pack()

        self._color_info.pack()

        # =====================================================
        # RESPONSIVE SCROLLING
        # =====================================================

        self._content_frame.bind(
            "<Configure>",
            self._on_content_configure,
        )

        self._scroll_canvas.bind(
            "<Configure>",
            self._on_canvas_configure,
        )

        self.bind(
            "<Configure>",
            self._on_panel_configure,
        )

        self._scroll_canvas.bind(
            "<MouseWheel>",
            self._on_mousewheel,
        )

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

    # =========================================================
    # RESPONSIVE SCROLLING
    # =========================================================

    def _on_content_configure(
        self,
        _event=None,
    ) -> None:

        self._scroll_canvas.configure(
            scrollregion=(
                self._scroll_canvas
                .bbox("all")
            )
        )

        self.after_idle(
            self._update_scrollbar
        )

    def _on_canvas_configure(
        self,
        event,
    ) -> None:

        self._scroll_canvas.itemconfigure(
            self._canvas_window,
            width=event.width,
        )

        self.after_idle(
            self._update_scrollbar
        )

    def _on_panel_configure(
        self,
        _event=None,
    ) -> None:

        self.after_idle(
            self._update_scrollbar
        )

    def _update_scrollbar(
        self,
    ) -> None:

        self.update_idletasks()

        content_height = (
            self._content_frame
            .winfo_reqheight()
        )

        available_height = (
            self._scroll_canvas
            .winfo_height()
        )

        # -----------------------------------------------------
        # Everything fits.
        # Hide the scrollbar.
        # -----------------------------------------------------

        if (
            available_height <= 1
            or content_height <= available_height
        ):

            self._scrollbar.place_forget()

            self._scroll_canvas.yview_moveto(
                0
            )

            return

        # -----------------------------------------------------
        # Content is larger than the available space.
        # Show the scrollbar without stealing width.
        # -----------------------------------------------------

        self._scrollbar.place(
            relx=1.0,
            rely=0.0,
            relheight=1.0,
            anchor=tk.NE,
        )

        self._scroll_canvas.configure(
            scrollregion=(
                self._scroll_canvas
                .bbox("all")
            )
        )

    # =========================================================
    # MOUSE WHEEL
    # =========================================================

    def _on_mousewheel(
        self,
        event,
    ) -> None:

        if not self._scrollbar.winfo_ismapped():
            return

        self._scroll_canvas.yview_scroll(
            int(
                -1 * (
                    event.delta / 120
                )
            ),
            "units",
        )