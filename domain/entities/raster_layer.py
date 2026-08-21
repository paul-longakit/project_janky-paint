from domain.value_objects.color import Color
from domain.value_objects.point import Point


class RasterLayer:

    def __init__(
        self,
        width: int,
        height: int,
    ):
        if width <= 0:
            raise ValueError(
                "Raster layer width must be greater than zero."
            )

        if height <= 0:
            raise ValueError(
                "Raster layer height must be greater than zero."
            )

        self.width = width
        self.height = height

        self.pixels: list[list[Color | None]] = [
            [None for _ in range(width)]
            for _ in range(height)
        ]

    def get_pixel(
        self,
        point: Point,
    ) -> Color | None:
        self._validate_point(point)

        return self.pixels[point.y][point.x]

    def set_pixel(
        self,
        point: Point,
        color: Color | None,
    ) -> None:
        self._validate_point(point)

        self.pixels[point.y][point.x] = color

    def _validate_point(
        self,
        point: Point,
    ) -> None:
        if not (
            0 <= point.x < self.width
            and 0 <= point.y < self.height
        ):
            raise IndexError(
                "Point is outside raster layer bounds."
            )