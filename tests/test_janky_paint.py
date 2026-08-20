from application.use_cases.add_layer import AddLayerUseCase
from application.use_cases.draw_stroke import DrawStrokeUseCase
from application.use_cases.save_asset import SaveAssetUseCase

from domain.entities.janky_paint import JankyPaint
from domain.value_objects.brush_settings import BrushSettings
from domain.value_objects.color import Color
from domain.value_objects.point import Point

from infrastructure.persistence.png_asset_repository import (
    PNGAssetRepository,
)

from infrastructure.rendering.pil_renderer import (
    PILRenderer,
)


paint = JankyPaint(400, 400)

add_layer = AddLayerUseCase()

add_layer.execute(
    paint,
    "Character",
)

draw_stroke = DrawStrokeUseCase()

draw_stroke.execute(
    paint=paint,
    points=[
        Point(50, 50),
        Point(100, 100),
        Point(150, 50),
    ],
    settings=BrushSettings(
        color=Color(255, 0, 0),
        size=10,
    ),
)


renderer = PILRenderer()
repository = PNGAssetRepository()

save_asset = SaveAssetUseCase(
    renderer=renderer,
    repository=repository,
)

save_asset.execute(
    paint=paint,
    path="output/test_asset.png",
)

print("PNG exported successfully.")