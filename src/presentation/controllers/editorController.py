from copy import deepcopy

from src.application.history.historyManager import HistoryManager

from src.application.useCases.fillAreaUseCase import FillAreaUseCase
from src.application.useCases.addLayerUseCase import AddLayerUseCase
from src.application.useCases.clearLayerUseCase import ClearLayerUseCase
from src.application.useCases.drawStrokeUseCase import DrawStrokeUseCase
from src.application.useCases.saveAssetUseCase import SaveAssetUseCase
from src.application.useCases.selectLayerUseCase import SelectLayerUseCase
from src.application.useCases.deleteLayerUseCase import DeleteLayerUseCase
from src.application.useCases.reorderLayerUseCase import ReorderLayerUseCase
from src.application.useCases.renameLayerUseCase import RenameLayerUseCase
from src.application.useCases.undoUseCase import UndoUseCase
from src.application.useCases.redoUseCase import RedoUseCase

from src.domain.entities.paintAppEntity import JankyPaintApp

from src.domain.enums.paintToolEnum import PaintTool

from src.domain.value_objects.pointValueObject import Point
from src.domain.value_objects.brushSettingsValueObject import BrushSettings
from src.domain.value_objects.colorValueObject import Color

from src.domain.abstractions.rendererAbstraction import Renderer

class EditorController:

    def __init__(
        self,
        paint: JankyPaintApp,
        renderer: Renderer,
        save_asset_use_case: SaveAssetUseCase,
        on_history_change=None,
    ):
        self.paint: JankyPaintApp = paint
        self.current_tool = PaintTool.BRUSH
        self.current_color = Color(0, 0, 0)
        self.current_brush_size = 5
        self.renderer = renderer
        self.save_asset_use_case = save_asset_use_case
        self.on_history_change = on_history_change

        self.history = HistoryManager()

        self.undo_use_case = UndoUseCase()
        self.redo_use_case = RedoUseCase()

        self.add_layer_use_case = AddLayerUseCase()
        self.select_layer_use_case = SelectLayerUseCase()
        self.delete_layer_use_case = DeleteLayerUseCase()
        self.draw_stroke_use_case = DrawStrokeUseCase(renderer)
        self.clear_layer_use_case = ClearLayerUseCase()
        self.fill_area_use_case = FillAreaUseCase(
            renderer=renderer,
        )
        self.reorder_layer_use_case = ReorderLayerUseCase()
        self.rename_layer_use_case = RenameLayerUseCase()

    def add_layer(self, name: str) -> None:

        self._execute_with_history(
            lambda: self.add_layer_use_case.execute(
                paint=self.paint,
                name=name,
            )
        )

    def select_layer(self, index: int) -> None:
        self.select_layer_use_case.execute(
            paint=self.paint,
            layer_index=index,
        )

    def rename_layer(
        self,
        index: int,
        name: str,
    ) -> None:

        self._execute_with_history(
            lambda: self.rename_layer_use_case.execute(
                paint=self.paint,
                index=index,
                name=name,
            )
        )

    def delete_layer(
        self,
        index: int,
    ) -> None:

        self._execute_with_history(
            lambda: self.delete_layer_use_case.execute(
                paint=self.paint,
                layer_index=index,
            )
        )

    def reorder_layer(
        self,
        from_index: int,
        to_index: int,
    ) -> None:

        self._execute_with_history(
            lambda: self.reorder_layer_use_case.execute(
                paint=self.paint,
                from_index=from_index,
                to_index=to_index,
            )
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

        self._execute_with_history(
            lambda: self.draw_stroke_use_case.execute(
                paint=self.paint,
                points=points,
                settings=settings,
            )
        )

    def clear_layer(self) -> None:

        self._execute_with_history(
            lambda: self.clear_layer_use_case.execute(
                paint=self.paint,
            )
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
    
    def fill_area(
        self,
        point: Point,
    ) -> None:

        self._execute_with_history(
            lambda: self.fill_area_use_case.execute(
                paint=self.paint,
                point=point,
                color=self.current_color,
            )
        )

    def pick_color(
        self,
        point: Point,
    ) -> None:

        color = self._sample_color_at_point(point)

        if color is not None:
            self.set_color(color)

            if hasattr(self, 'on_history_change') and self.on_history_change:
                self.on_history_change()

    def _sample_color_at_point(
        self,
        point: Point,
    ):

        for layer in reversed(self.paint.layers):

            if not layer.visible:
                continue

            try:
                pixel = layer.image.getpixel(
                    (point.x, point.y)
                )

                if len(pixel) == 4:
                    r, g, b, a = pixel

                    if a == 0:
                        continue

                    return Color(r, g, b, a)

            except IndexError:
                continue

        return None

    def _execute_with_history(
        self,
        operation,
    ) -> None:

        before = deepcopy(
            self.paint
        )

        operation()

        after = deepcopy(
            self.paint
        )

        self.history.record(
            before=before,
            after=after,
        )

        if self.on_history_change:
            self.on_history_change()

    def undo(self) -> bool:

        result = self.undo_use_case.execute(
            paint=self.paint,
            history=self.history,
        )

        if result and self.on_history_change:
            self.on_history_change()

        return result

    def redo(self) -> bool:

        result = self.redo_use_case.execute(
            paint=self.paint,
            history=self.history,
        )

        if result and self.on_history_change:
            self.on_history_change()

        return result

    def can_undo(self) -> bool:

        return self.history.can_undo()

    def can_redo(self) -> bool:

        return self.history.can_redo()