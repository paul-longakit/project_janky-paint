import tkinter as tk

from src.domain.enums.paintToolEnum import PaintTool
from src.domain.value_objects.pointValueObject import Point


class CanvasController:

    def __init__(
        self,
        editor_controller,
        canvas_view,
    ):
        self.editor_controller = editor_controller
        self.canvas_view = canvas_view

        self.is_drawing = False
        self.current_points: list[Point] = []
        self.preview_ids: list[int] = []

        self._bind_events()

    # =============================================================
    # EVENT BINDING
    # =============================================================

    def _bind_events(self) -> None:

        self.canvas_view.bind(
            "<Button-1>",
            self._on_stroke_start,
        )

        self.canvas_view.bind(
            "<B1-Motion>",
            self._on_stroke_continue,
        )

        self.canvas_view.bind(
            "<ButtonRelease-1>",
            self._on_stroke_finish,
        )

    # =============================================================
    # STROKE HANDLERS
    # =============================================================

    def _on_stroke_start(self, event) -> None:

        if self.editor_controller.current_tool == PaintTool.BUCKET:
            self.editor_controller.fill_area(
                Point(event.x, event.y)
            )

            self.refresh()
            return

        if self.editor_controller.current_tool == PaintTool.EYEDROPPER:
            self.editor_controller.pick_color(
                Point(event.x, event.y)
            )

            self.refresh()
            return

        self.is_drawing = True

        self.current_points = [
            Point(event.x, event.y)
        ]

        self.preview_ids = []

    def _on_stroke_continue(self, event) -> None:

        if not self.is_drawing:
            return

        previous_point = self.current_points[-1]

        current_point = Point(
            event.x,
            event.y,
        )

        self.current_points.append(
            current_point
        )

        preview_id = self.canvas_view.draw_preview_line(
            previous_point.x,
            previous_point.y,
            current_point.x,
            current_point.y,
            self._preview_color(),
            self.editor_controller.current_brush_size,
        )

        self.preview_ids.append(
            preview_id
        )

    def _on_stroke_finish(self, event) -> None:

        if not self.is_drawing:
            return

        self.current_points.append(
            Point(event.x, event.y)
        )

        self.editor_controller.draw_stroke(
            points=self.current_points
        )

        self.is_drawing = False
        self.current_points = []

        self._clear_preview()

        self.refresh()

    # =============================================================
    # CANVAS
    # =============================================================

    def refresh(self) -> None:

        image = self.editor_controller.render()

        self.canvas_view.display_image(
            image
        )

    def _clear_preview(self) -> None:

        for preview_id in self.preview_ids:
            self.canvas_view.remove_preview(
                preview_id
            )

        self.preview_ids = []

    # =============================================================
    # PREVIEW
    # =============================================================

    def _preview_color(self) -> str:

        if self.editor_controller.current_tool == PaintTool.ERASER:
            return "white"

        color = self.editor_controller.current_color

        return (
            f"#{color.red:02x}"
            f"{color.green:02x}"
            f"{color.blue:02x}"
        )