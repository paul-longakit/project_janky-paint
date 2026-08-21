from src.application.useCases.fillAreaUseCase import FillAreaUseCase
from src.application.useCases.addLayerUseCase import AddLayerUseCase
from src.application.useCases.clearLayerUseCase import ClearLayerUseCase
from src.application.useCases.drawStrokeUseCase import DrawStrokeUseCase
from src.application.useCases.saveAssetUseCase import SaveAssetUseCase
from src.application.useCases.selectLayerUseCase import SelectLayerUseCase
from src.application.useCases.deleteLayerUseCase import DeleteLayerUseCase


from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.value_objects.brushSettingsValueObject import BrushSettings
from src.domain.value_objects.colorValueObject import Color
from src.domain.enums.paintToolEnum import PaintTool
from src.domain.value_objects.pointValueObject import Point

from src.domain.abstractions.rendererAbstraction import Renderer

class EditorController:

    def __init__(
        self,
        paint: JankyPaintApp,
        renderer: Renderer,
        save_asset_use_case: SaveAssetUseCase,
    ):
        self.paint: JankyPaintApp = paint
        self.current_tool = PaintTool.BRUSH
        self.current_color = Color(0, 0, 0)
        self.current_brush_size = 5
        self.renderer = renderer
        self.save_asset_use_case = save_asset_use_case

        self.add_layer_use_case = AddLayerUseCase()
        self.select_layer_use_case = SelectLayerUseCase()
        self.delete_layer_use_case = DeleteLayerUseCase()
        self.draw_stroke_use_case = DrawStrokeUseCase(renderer)
        self.clear_layer_use_case = ClearLayerUseCase()
        self.fill_area_use_case = FillAreaUseCase(
            renderer=renderer,
        )

    def add_layer(self, name: str) -> None:
        self.add_layer_use_case.execute(
            paint=self.paint,
            name=name,
        )

    def select_layer(self, index: int) -> None:
        self.select_layer_use_case.execute(
            paint=self.paint,
            layer_index=index,
        )

    def delete_layer(self, index: int) -> None:
        self.delete_layer_use_case.execute(
            paint=self.paint,
            layer_index=index,
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