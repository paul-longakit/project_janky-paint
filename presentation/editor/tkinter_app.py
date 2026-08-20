import tkinter as tk

from PIL import ImageTk

from application.use_cases.create_document import CreateDocumentUseCase
from application.use_cases.save_asset import SaveAssetUseCase

from infrastructure.persistence.png_asset_repository import PNGAssetRepository
from infrastructure.rendering.pil_renderer import PILRenderer

from presentation.editor.editor_controller import EditorController
from presentation.editor.color_panel import ColorPanel

from domain.value_objects.color import Color
from domain.value_objects.paint_tool import PaintTool
from domain.value_objects.point import Point


class JankyPaintApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JankyPaint 95")

        # =========================================================
        # APPLICATION / DOMAIN SETUP
        # =========================================================

        paint = CreateDocumentUseCase().execute(width=400, height=400)

        renderer = PILRenderer()
        repository = PNGAssetRepository()

        save_asset = SaveAssetUseCase(
            renderer=renderer,
            repository=repository,
        )

        self.controller = EditorController(
            paint=paint,
            renderer=renderer,
            save_asset_use_case=save_asset,
        )

        # =========================================================
        # TOOLBAR
        # =========================================================

        self.toolbar = tk.Frame(root, relief=tk.RAISED, bd=2)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self._build_tool_buttons()
        self._build_brush_size_slider()
        self._build_color_panel()

        # =========================================================
        # CANVAS
        # =========================================================

        self.canvas = tk.Canvas(
            root,
            width=400,
            height=400,
            bg="white",
            cursor="crosshair",
        )

        self.canvas.pack(padx=10, pady=10)

        # =========================================================
        # DRAWING STATE
        # =========================================================

        self.is_drawing = False
        self.current_points: list[Point] = []
        self.preview_ids: list[int] = []

        # =========================================================
        # MOUSE EVENTS
        # =========================================================

        self.canvas.bind("<Button-1>", self._on_stroke_start)
        self.canvas.bind("<B1-Motion>", self._on_stroke_continue)
        self.canvas.bind("<ButtonRelease-1>", self._on_stroke_finish)

        # =========================================================
        # LAYER CONTROL
        # =========================================================

        tk.Button(
            root,
            text="Add Layer",
            command=self._add_layer,
        ).pack()

        # =========================================================
        # INITIAL CANVAS RENDER
        # =========================================================

        self._refresh_canvas()

    # =========================================================
    # TOOLBAR BUILDERS
    # =========================================================

    def _build_tool_buttons(self) -> None:
        tk.Button(
            self.toolbar,
            text="🖌 Brush",
            command=self._use_brush,
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            self.toolbar,
            text="🧼 Eraser",
            command=self._use_eraser,
        ).pack(fill=tk.X, pady=2)

    def _build_brush_size_slider(self) -> None:
        tk.Label(self.toolbar, text="Size:").pack(pady=(15, 2))

        self.size_slider = tk.Scale(
            self.toolbar,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            command=self._on_brush_size_change,
        )

        self.size_slider.set(self.controller.current_brush_size)
        self.size_slider.pack(fill=tk.X)

    def _build_color_panel(self) -> None:
        self.color_panel = ColorPanel(
            parent=self.toolbar,
            initial_color=self.controller.current_color,
            on_color_change=self._on_color_change,
        )

        self.color_panel.pack(fill=tk.X, pady=10)

    # =========================================================
    # TOOL HANDLERS
    # =========================================================

    def _use_brush(self) -> None:
        self.controller.set_tool(PaintTool.BRUSH)

    def _use_eraser(self) -> None:
        self.controller.set_tool(PaintTool.ERASER)

    def _on_brush_size_change(self, value: str) -> None:
        self.controller.set_brush_size(int(value))

    def _on_color_change(self, color: Color) -> None:
        self.controller.set_color(color)

    # =========================================================
    # LAYER HANDLERS
    # =========================================================

    def _add_layer(self) -> None:
        layer_number = len(self.controller.paint.layers) + 1
        self.controller.add_layer(f"Layer {layer_number}")

    # =========================================================
    # STROKE HANDLERS
    # =========================================================

    def _on_stroke_start(self, event) -> None:
        self.is_drawing = True
        self.current_points = [Point(event.x, event.y)]
        self.preview_ids = []

    def _on_stroke_continue(self, event) -> None:
        if not self.is_drawing:
            return

        previous_point = self.current_points[-1]
        current_point = Point(event.x, event.y)

        self.current_points.append(current_point)

        preview_id = self.canvas.create_line(
            previous_point.x,
            previous_point.y,
            current_point.x,
            current_point.y,
            fill=self._preview_color(),
            width=self.controller.current_brush_size,
            capstyle=tk.ROUND,
            smooth=True,
        )

        self.preview_ids.append(preview_id)

    def _on_stroke_finish(self, event) -> None:
        if not self.is_drawing:
            return

        self.current_points.append(Point(event.x, event.y))

        self.controller.draw_stroke(points=self.current_points)

        self.is_drawing = False
        self.current_points = []

        self._clear_preview()
        self._refresh_canvas()

    # =========================================================
    # CANVAS RENDERING
    # =========================================================

    def _refresh_canvas(self) -> None:
        image = self.controller.render()

        self.tk_image = ImageTk.PhotoImage(image)

        self.canvas.delete("all")

        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.tk_image
        )

    def _clear_preview(self) -> None:
        for preview_id in self.preview_ids:
            self.canvas.delete(preview_id)

        self.preview_ids = []

    def _preview_color(self) -> str:
        if self.controller.current_tool == PaintTool.ERASER:
            return "white"

        color = self.controller.current_color

        return (
            f"#{color.red:02x}"
            f"{color.green:02x}"
            f"{color.blue:02x}"
        )