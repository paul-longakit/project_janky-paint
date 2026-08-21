from application.use_cases.fillAreaUseCase import FillAreaUseCase
from application.use_cases.addLayerUseCase import AddLayerUseCase
from application.use_cases.clearLayerUseCase import ClearLayerUseCase
from application.use_cases.drawStrokeUseCase import DrawStrokeUseCase
from application.use_cases.saveAssetUseCase import SaveAssetUseCase
from application.use_cases.selectLayerUseCase import SelectLayerUseCase


from domain.entities.paintAppEntity import JankyPaint
from domain.value_objects.brushSettingsValueObject import BrushSettings
from domain.value_objects.colorValueObject import Color
from domain.enums.paintToolEnum import PaintTool
from domain.value_objects.pointValueObject import Point



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
        self.fill_area_use_case = FillAreaUseCase()

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
    
    def fill_area(self, point: Point) -> None:
        self.fill_area_use_case.execute(
            paint=self.paint,
            point=point,
            color=self.current_color,
        )