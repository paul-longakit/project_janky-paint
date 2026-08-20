from PIL import Image, ImageChops, ImageDraw

from domain.entities.janky_paint import JankyPaint
from domain.entities.layer import Layer
from domain.entities.stroke import Stroke
from domain.value_objects.paint_tool import PaintTool


class PILRenderer:

    def render(self, paint: JankyPaint) -> Image.Image:
        image = Image.new(
            "RGBA",
            (paint.width, paint.height),
            (0, 0, 0, 0),
        )

        for layer in paint.layers:
            layer_image = Image.new(
                "RGBA",
                (paint.width, paint.height),
                (0, 0, 0, 0),
            )

            self._render_layer(
                layer_image,
                layer,
            )

            image = Image.alpha_composite(
                image,
                layer_image,
            )

        return image

    def _render_layer(
        self,
        image: Image.Image,
        layer: Layer,
    ) -> None:

        for stroke in layer.strokes:
            self._render_stroke(
                image,
                stroke,
            )

    def _render_stroke(
        self,
        image: Image.Image,
        stroke: Stroke,
    ) -> None:

        points = [
            (point.x, point.y)
            for point in stroke.points
        ]

        if len(points) == 1:
            points = [
                points[0],
                points[0],
            ]

        if stroke.settings.tool == PaintTool.BRUSH:
            self._draw_brush(
                image,
                points,
                stroke,
            )

        elif stroke.settings.tool == PaintTool.ERASER:
            self._draw_eraser(
                image,
                points,
                stroke,
            )

    def _draw_brush(
        self,
        image: Image.Image,
        points: list[tuple[int, int]],
        stroke: Stroke,
    ) -> None:

        draw = ImageDraw.Draw(image)

        color = (
            stroke.settings.color.red,
            stroke.settings.color.green,
            stroke.settings.color.blue,
            stroke.settings.color.alpha,
        )

        draw.line(
            points,
            fill=color,
            width=stroke.settings.size,
            joint="curve",
        )

    def _draw_eraser(
        self,
        image: Image.Image,
        points: list[tuple[int, int]],
        stroke: Stroke,
    ) -> None:

        # Create a grayscale mask representing
        # the area that should be erased.
        mask = Image.new(
            "L",
            image.size,
            0,
        )

        mask_draw = ImageDraw.Draw(mask)

        mask_draw.line(
            points,
            fill=255,
            width=stroke.settings.size,
            joint="curve",
        )

        # Get the current alpha channel.
        current_alpha = image.getchannel("A")

        # Remove the erased area from the alpha.
        new_alpha = ImageChops.subtract(
            current_alpha,
            mask,
        )

        image.putalpha(new_alpha)