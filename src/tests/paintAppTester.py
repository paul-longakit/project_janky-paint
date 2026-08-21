from application.useCases.addLayerUseCase import AddLayerUseCase
from application.useCases.drawStrokeUseCase import DrawStrokeUseCase
from application.useCases.saveAssetUseCase import SaveAssetUseCase

from domain.entities.paintAppEntity import JankyPaintApp
from src.domain.value_objects.brushSettingsValueObject import BrushSettings
from src.domain.value_objects.colorValueObject import Color
from src.domain.value_objects.pointValueObject import Point

from src.infrastructure.persistence.pngAssetRepositoryPersistence import (
    PNGAssetRepository,
)

from src.infrastructure.rendering.pilRendererRendering import (
    PILRenderer,
)


paint = JankyPaintApp(400, 400)

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