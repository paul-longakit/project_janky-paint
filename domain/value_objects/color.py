from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __post_init__(self):
        values = (
            self.red,
            self.green,
            self.blue,
            self.alpha,
        )

        if any(value < 0 or value > 255 for value in values):
            raise ValueError(
                "Color values must be between 0 and 255."
            )