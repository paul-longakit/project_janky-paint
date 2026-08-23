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
        on_rename,
        on_delete,
    ):
        self.index = index
        self.on_rename = on_rename

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
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=5,
            pady=4,
        )

        tk.Button(
            self.frame,
            text="-",
            width=1,
            height=1,
            fg="white",
            bg="#d9534f",
            activeforeground="white",
            activebackground="#c9302c",
            command=lambda: on_delete(
                self.index
            ),
        ).pack(
            side=tk.RIGHT,
            padx=3,
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

        # =========================================================
        # RENAME
        # =========================================================

        self.label.bind(
            "<Double-Button-1>",
            self._start_rename,
        )

    # =============================================================
    # RENAME
    # =============================================================

    def _start_rename(
        self,
        event,
    ):

        current_name = self.label.cget("text")

        self.label.pack_forget()

        self.rename_entry = tk.Entry(
            self.frame,
        )

        self.rename_entry.insert(
            0,
            current_name,
        )

        self.rename_entry.select_range(
            0,
            tk.END,
        )

        self.rename_entry.pack(
            fill=tk.X,
            padx=3,
            pady=2,
        )

        self.rename_entry.focus_set()

        self.rename_entry.bind(
            "<Return>",
            self._confirm_rename,
        )

        self.rename_entry.bind(
            "<Escape>",
            self._cancel_rename,
        )

        self.rename_entry.bind(
            "<FocusOut>",
            self._confirm_rename,
        )

    def _confirm_rename(
        self,
        event=None,
    ):

        if not hasattr(
            self,
            "rename_entry",
        ):
            return

        name = self.rename_entry.get().strip()

        if not name:
            self._cancel_rename()
            return

        self.on_rename(
            self.index,
            name,
        )

    def _cancel_rename(
        self,
        event=None,
    ):

        if not hasattr(
            self,
            "rename_entry",
        ):
            return

        self.rename_entry.destroy()

        del self.rename_entry

        self.label.pack(
            fill=tk.X,
            padx=5,
            pady=4,
        )

    # =============================================================
    # DISPLAY
    # =============================================================

    def pack(self) -> None:

        self.frame.pack(
            fill=tk.X,
            padx=5,
            pady=1,
        )

    def destroy(self) -> None:

        self.frame.destroy()