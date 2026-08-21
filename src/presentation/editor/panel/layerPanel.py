import tkinter as tk


class LayerPanel(tk.Frame):

    def __init__(
        self,
        parent,
        controller,
        on_layer_change=None,
    ):
        super().__init__(
            parent,
            relief=tk.RAISED,
            bd=2,
        )

        self.controller = controller
        self.on_layer_change = on_layer_change

        self._build_header()
        self._build_layer_list()
        self._build_controls()

        self.refresh()

    # =========================================================
    # UI BUILDERS
    # =========================================================

    def _build_header(self) -> None:
        tk.Label(
            self,
            text="Layers",
            font=("Arial", 10, "bold"),
        ).pack(
            fill=tk.X,
            padx=5,
            pady=(5, 2),
        )

    def _build_layer_list(self) -> None:
        self.layer_list = tk.Listbox(
            self,
            height=10,
            exportselection=False,
        )

        self.layer_list.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5,
        )

        self.layer_list.bind(
            "<<ListboxSelect>>",
            self._on_layer_selected,
        )

    def _build_controls(self) -> None:
        controls = tk.Frame(self)
        controls.pack(
            fill=tk.X,
            padx=5,
            pady=(0, 5),
        )

        tk.Button(
            controls,
            text="+",
            command=self._add_layer,
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=1,
        )

        tk.Button(
            controls,
            text="-",
            command=self._delete_layer,
        ).pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=1,
        )

    # =========================================================
    # LAYER ACTIONS
    # =========================================================

    def _add_layer(self) -> None:
        layer_number = len(
            self.controller.paint.layers
        ) + 1

        self.controller.add_layer(
            f"Layer {layer_number}"
        )

        self.refresh()

        self._notify_layer_change()

    def _delete_layer(self) -> None:
        paint = self.controller.paint

        if len(paint.layers) <= 1:
            return

        if paint.active_layer_index is None:
            return

        self.controller.delete_layer(
            paint.active_layer_index
        )

        self.refresh()

        self._notify_layer_change()

    def _on_layer_selected(self, event) -> None:
        selection = self.layer_list.curselection()

        if not selection:
            return

        index = selection[0]

        self.controller.select_layer(index)

        self._notify_layer_change()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self) -> None:
        self.layer_list.delete(
            0,
            tk.END,
        )

        layers = self.controller.paint.layers
        active_index = self.controller.paint.active_layer_index

        for index, layer in enumerate(layers):
            prefix = "● " if index == active_index else "   "

            self.layer_list.insert(
                tk.END,
                f"{prefix}{layer.name}",
            )

        if active_index is not None:
            self.layer_list.selection_set(
                active_index
            )

            self.layer_list.activate(
                active_index
            )

    # =========================================================
    # CALLBACK
    # =========================================================

    def _notify_layer_change(self) -> None:
        if self.on_layer_change:
            self.on_layer_change()