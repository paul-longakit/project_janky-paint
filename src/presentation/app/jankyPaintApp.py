import tkinter as tk

from src.application.useCases.createDocumentUseCase import CreateDocumentUseCase
from src.application.useCases.saveAssetUseCase import SaveAssetUseCase

from src.infrastructure.persistence.pngAssetRepositoryPersistence import PNGAssetRepository
from src.infrastructure.rendering.pilRendererRendering import PILRenderer

from src.presentation.controllers.canvasController import CanvasController
from src.presentation.controllers.editorController import EditorController
from src.presentation.controllers.layerController import LayerController

from src.presentation.views.editor.editorView import EditorView

from src.domain.enums.paintToolEnum import PaintTool
from src.domain.value_objects.colorValueObject import Color


class JankyPaintApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JankyPaint 95")

        # =========================================================
        # UNDO / REDO SHORTCUTS
        # =========================================================

        self.root.bind(
            "<Control-z>",
            self._undo,
        )

        self.root.bind(
            "<Control-y>",
            self._redo,
        )

        self.root.bind(
            "<Control-Shift-Z>",
            self._redo,
        )

        # =========================================================
        # APPLICATION / DOMAIN SETUP
        # =========================================================

        paint = CreateDocumentUseCase().execute(
            width=400,
            height=400,
        )

        renderer = PILRenderer()
        repository = PNGAssetRepository()

        save_asset = SaveAssetUseCase(
            renderer=renderer,
            repository=repository,
        )

        # =========================================================
        # CONTROLLERS
        # =========================================================
        
        self.controller = EditorController(
            paint=paint,
            renderer=renderer,
            save_asset_use_case=save_asset,
            on_history_change=self._update_history_buttons,
        )

        self.layer_controller = LayerController(
            editor_controller=self.controller,
        )


        # =========================================================
        # EDITOR VIEW
        # =========================================================

        self.view = EditorView(
            root=self.root,
            controller=self.controller,
            layer_controller=self.layer_controller,

            on_undo=self._undo,
            on_redo=self._redo,

            on_color_change=self._on_color_change,
            on_layer_change=self._on_layer_change,

            on_brush=self._use_brush,
            on_eraser=self._use_eraser,
            on_bucket=self._use_bucket,
            on_eyedropper=self._use_eyedropper,

            on_brush_size_change=(
                self._on_brush_size_change
            ),
        )

        # =========================================================
        # INITIAL CANVAS RENDER
        # =========================================================

        self._refresh_canvas()
        self._update_history_buttons()

        self.canvas_controller = CanvasController(
            editor_controller=self.controller,
            canvas_view=self.view.canvas_view,
        )
    # =============================================================
    # TOOL HANDLERS
    # =============================================================

    def _use_brush(self) -> None:
        self.controller.set_tool(
            PaintTool.BRUSH
        )

    def _use_eraser(self) -> None:
        self.controller.set_tool(
            PaintTool.ERASER
        )

    def _use_bucket(self) -> None:
        self.controller.set_tool(
            PaintTool.BUCKET
        )

    def _use_eyedropper(self) -> None:
        self.controller.set_tool(
            PaintTool.EYEDROPPER
        )

    def _on_brush_size_change(
        self,
        value: str,
    ) -> None:

        self.controller.set_brush_size(
            int(value)
        )

    # =============================================================
    # EDITOR HANDLERS
    # =============================================================

    def _on_color_change(
        self,
        color: Color,
    ) -> None:

        self.controller.set_color(
            color
        )

    def _on_layer_change(self) -> None:
        self._refresh_canvas()

    # =============================================================
    # CANVAS RENDERING
    # =============================================================

    def _refresh_canvas(self) -> None:

        image = self.controller.render()

        self.view.canvas_view.display_image(
            image
        )

    # =============================================================
    # HISTORY
    # =============================================================

    def _undo(
        self,
        event=None,
    ) -> str:

        if self.controller.undo():

            self.view.refresh_layers()
            self._refresh_canvas()

        return "break"

    def _redo(
        self,
        event=None,
    ) -> str:

        if self.controller.redo():

            self.view.layer_view.refresh()

            self._refresh_canvas()

        return "break"

    def _update_history_buttons(self) -> None:

        self.view.set_history_state(
            can_undo=self.controller.can_undo(),
            can_redo=self.controller.can_redo(),
        )