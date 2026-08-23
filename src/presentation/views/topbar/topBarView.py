import tkinter as tk


class TopBarView:

    def __init__(
        self,
        parent,
        on_undo,
        on_redo,
    ):
        self.parent = parent

        self.on_undo = on_undo
        self.on_redo = on_redo

        self._frame = tk.Frame(
            parent,
            relief=tk.RAISED,
            bd=1,
        )

        # =========================================================
        # LEFT SIDE
        # =========================================================

        self._menu_frame = tk.Frame(
            self._frame,
        )

        self._menu_frame.pack(
            side=tk.LEFT,
            fill=tk.Y,
        )

        self._build_menus()

        # =========================================================
        # RIGHT SIDE
        # =========================================================

        self._action_frame = tk.Frame(
            self._frame,
        )

        self._action_frame.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self._build_actions()

    # =============================================================
    # MENUS
    # =============================================================

    def _build_menus(self) -> None:

        self._build_file_menu()
        self._build_edit_menu()
        self._build_view_menu()
        self._build_image_menu()
        self._build_layer_menu()
        self._build_help_menu()

    def _create_menu_button(
        self,
        text: str,
        menu,
    ) -> None:

        button = tk.Menubutton(
            self._menu_frame,
            text=text,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            menu=menu,
        )

        button.pack(
            side=tk.LEFT,
        )

    def _build_file_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="New",
        )

        menu.add_command(
            label="Open",
        )

        menu.add_separator()

        menu.add_command(
            label="Save",
        )

        menu.add_command(
            label="Save As...",
        )

        menu.add_separator()

        menu.add_command(
            label="Exit",
            command=self.parent.quit,
        )

        self._create_menu_button(
            "File",
            menu,
        )

    def _build_edit_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="Undo",
            command=self.on_undo,
        )

        menu.add_command(
            label="Redo",
            command=self.on_redo,
        )

        menu.add_separator()

        menu.add_command(
            label="Cut",
        )

        menu.add_command(
            label="Copy",
        )

        menu.add_command(
            label="Paste",
        )

        self._create_menu_button(
            "Edit",
            menu,
        )

    def _build_view_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="Zoom In",
        )

        menu.add_command(
            label="Zoom Out",
        )

        menu.add_command(
            label="Reset Zoom",
        )

        self._create_menu_button(
            "View",
            menu,
        )

    def _build_image_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="Image Size",
        )

        menu.add_command(
            label="Canvas Size",
        )

        self._create_menu_button(
            "Image",
            menu,
        )

    def _build_layer_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="New Layer",
        )

        menu.add_command(
            label="Delete Layer",
        )

        menu.add_command(
            label="Rename Layer",
        )

        menu.add_separator()

        menu.add_command(
            label="Move Up",
        )

        menu.add_command(
            label="Move Down",
        )

        self._create_menu_button(
            "Layer",
            menu,
        )

    def _build_help_menu(self) -> None:

        menu = tk.Menu(
            self._menu_frame,
            tearoff=False,
        )

        menu.add_command(
            label="About JankyPaint",
        )

        self._create_menu_button(
            "Help",
            menu,
        )

    # =============================================================
    # ACTIONS
    # =============================================================

    def _build_actions(self) -> None:

        self.undo_button = tk.Button(
            self._action_frame,
            text="Undo ↶",
            width=3,
            command=self.on_undo,
        )

        self.undo_button.pack(
            side=tk.LEFT,
            padx=2,
            pady=2,
        )

        self.redo_button = tk.Button(
            self._action_frame,
            text="Redo ↷",
            width=3,
            command=self.on_redo,
        )

        self.redo_button.pack(
            side=tk.LEFT,
            padx=2,
            pady=2,
        )

    # =============================================================
    # HISTORY STATE
    # =============================================================

    def set_history_state(
        self,
        can_undo: bool,
        can_redo: bool,
    ) -> None:

        self.undo_button.configure(
            state=(
                tk.NORMAL
                if can_undo
                else tk.DISABLED
            )
        )

        self.redo_button.configure(
            state=(
                tk.NORMAL
                if can_redo
                else tk.DISABLED
            )
        )

    # =============================================================
    # WIDGET
    # =============================================================

    def get_widget(self) -> tk.Frame:

        return self._frame