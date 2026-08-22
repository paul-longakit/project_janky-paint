import tkinter as tk


class ToolbarView:

    def __init__(
        self,
        parent,
        current_brush_size: int,
        on_brush,
        on_eraser,
        on_bucket,
        on_brush_size_change,
    ):
        self.toolbar = tk.Frame(
            parent,
            relief=tk.RAISED,
            bd=2,
        )

        self.toolbar.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=5,
            pady=5,
        )

        self._build_tool_buttons(
            on_brush=on_brush,
            on_eraser=on_eraser,
            on_bucket=on_bucket,
        )

        self._build_brush_size_slider(
            current_brush_size=current_brush_size,
            on_brush_size_change=on_brush_size_change,
        )

    # =============================================================
    # TOOL BUTTONS
    # =============================================================

    def _build_tool_buttons(
        self,
        on_brush,
        on_eraser,
        on_bucket,
    ) -> None:

        tk.Button(
            self.toolbar,
            text="🖌 Brush",
            command=on_brush,
        ).pack(
            fill=tk.X,
            pady=2,
        )

        tk.Button(
            self.toolbar,
            text="🧼 Eraser",
            command=on_eraser,
        ).pack(
            fill=tk.X,
            pady=2,
        )

        tk.Button(
            self.toolbar,
            text="🪣 Bucket",
            command=on_bucket,
        ).pack(
            fill=tk.X,
            pady=2,
        )

    # =============================================================
    # BRUSH SETTINGS
    # =============================================================

    def _build_brush_size_slider(
        self,
        current_brush_size: int,
        on_brush_size_change,
    ) -> None:

        tk.Label(
            self.toolbar,
            text="Size:",
        ).pack(
            pady=(15, 2),
        )

        self.size_slider = tk.Scale(
            self.toolbar,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            command=on_brush_size_change,
        )

        self.size_slider.set(
            current_brush_size
        )

        self.size_slider.pack(
            fill=tk.X,
        )