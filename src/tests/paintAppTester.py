from application.use_cases.addLayerUseCase import AddLayerUseCase
from application.use_cases.drawStrokeUseCase import DrawStrokeUseCase
from application.use_cases.saveAssetUseCase import SaveAssetUseCase

from domain.entities.paintAppEntity import JankyPaint
from domain.value_objects.brushSettingsValueObject import BrushSettings
from domain.value_objects.colorValueObject import Color
from domain.value_objects.pointValueObject import Point

from infrastructure.persistence.pngAssetRepositoryPersistence import (
    PNGAssetRepository,
)

from infrastructure.rendering.pilRendererRendering import (
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

paint.fill_area(
    point=Point(200, 200),
    color=Color(255, 0, 0),
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