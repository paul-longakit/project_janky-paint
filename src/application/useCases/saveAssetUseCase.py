from src.domain.entities.paintAppEntity import JankyPaintApp


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
        paint: JankyPaintApp,
        path: str,
    ) -> None:

        image = self.renderer.render(paint)

        self.repository.save(
            image,
            path,
        )