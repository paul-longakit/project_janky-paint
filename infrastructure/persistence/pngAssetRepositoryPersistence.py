from pathlib import Path

from PIL import Image


class PNGAssetRepository:

    def save(
        self,
        image: Image.Image,
        path: str,
    ) -> None:

        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        image.save(
            file_path,
            format="PNG",
        )