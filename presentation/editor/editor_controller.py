from application.use_cases.add_layer import AddLayerUseCase
from application.use_cases.clear_layer import ClearLayerUseCase
from application.use_cases.draw_stroke import DrawStrokeUseCase
from application.use_cases.save_asset import SaveAssetUseCase
from application.use_cases.select_layer import SelectLayerUseCase

from domain.entities.janky_paint import JankyPaint
from domain.value_objects.brush_settings import BrushSettings
from domain.value_objects.color import Color
from domain.value_objects.paint_tool import PaintTool
from domain.value_objects.point import Point


class EditorController:

    def __init__(
        self,
        paint: JankyPaint,
        renderer,
        save_asset_use_case: SaveAssetUseCase,
    ):
        self.paint: JankyPaint = paint
        self.current_tool = PaintTool.BRUSH
        self.current_color = Color(0, 0, 0)
        self.current_brush_size = 5
        self.renderer = renderer
        self.save_asset_use_case = save_asset_use_case

        self.add_layer_use_case = AddLayerUseCase()
        self.select_layer_use_case = SelectLayerUseCase()
        self.draw_stroke_use_case = DrawStrokeUseCase()
        self.clear_layer_use_case = ClearLayerUseCase()

    def add_layer(self, name: str) -> None:
        self.add_layer_use_case.execute(
            paint=self.paint,
            name=name,
        )

    def select_layer(self, index: int) -> None:
        self.select_layer_use_case.execute(
            paint=self.paint,
            index=index,
        )

    def draw_stroke(
        self,
        points: list[Point],
    ) -> None:

        settings = BrushSettings(
            color=self.current_color,
            size=self.current_brush_size,
            tool=self.current_tool,
        )

        self.draw_stroke_use_case.execute(
            paint=self.paint,
            points=points,
            settings=settings,
        )

    def clear_layer(self) -> None:
        self.clear_layer_use_case.execute(
            paint=self.paint,
        )

    def save(self, path: str) -> None:
        self.save_asset_use_case.execute(
            paint=self.paint,
            path=path,
        )

    def render(self):
        return self.renderer.render(
            self.paint,
        )

    def set_tool(self, tool: PaintTool) -> None:
        self.current_tool = tool

    def set_color(self, color: Color) -> None:
        self.current_color = color

    def set_brush_size(self, size: int) -> None:
        self.current_brush_size = size