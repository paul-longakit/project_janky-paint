import tkinter as tk


class LayerItemView:

    def __init__(
        self,
        parent,
        index: int,
        name: str,
        active: bool,
        on_mouse_down,
        on_mouse_move,
        on_mouse_up,
    ):
        self.index = index

        self.frame = tk.Frame(
            parent,
            relief=tk.SUNKEN if active else tk.RAISED,
            bd=1,
        )

        self.label = tk.Label(
            self.frame,
            text=name,
            anchor=tk.W,
        )

        self.label.pack(
            fill=tk.X,
            padx=5,
            pady=4,
        )

        # =========================================================
        # MOUSE EVENTS
        # =========================================================

        for widget in (
            self.frame,
            self.label,
        ):

            widget.bind(
                "<ButtonPress-1>",
                lambda event: on_mouse_down(
                    self.index,
                    event,
                ),
            )

            widget.bind(
                "<B1-Motion>",
                lambda event: on_mouse_move(
                    self.index,
                    event,
                ),
            )

            widget.bind(
                "<ButtonRelease-1>",
                lambda event: on_mouse_up(
                    self.index,
                    event,
                ),
            )

    def pack(self) -> None:

        self.frame.pack(
            fill=tk.X,
            padx=5,
            pady=1,
        )

    def destroy(self) -> None:

        self.frame.destroy()