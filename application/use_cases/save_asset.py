from domain.entities.janky_paint import JankyPaint


class SaveAssetUseCase:

    def __init__(
        self,
        renderer,
        repository,
    ):
        self.renderer = renderer
        self.repository = repository

    def execute(
        self,
        paint: JankyPaint,
        path: str,
    ) -> None:

        image = self.renderer.render(paint)

        self.repository.save(
            image,
            path,
        )