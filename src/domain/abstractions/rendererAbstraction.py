from abc import ABC, abstractmethod

from PIL import Image

from src.domain.entities.paintAppEntity import JankyPaintApp
from src.domain.entities.layerEntity import Layer


class Renderer(ABC):

    @abstractmethod
    def render(
        self,
        paint: JankyPaintApp,
    ) -> Image.Image:
        pass

    @abstractmethod
    def render_operation(
        self,
        layer: Layer,
        operation,
    ) -> None:
        pass