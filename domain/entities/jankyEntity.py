class LoreEntity:
    def __init__(
        self,
        name: str,
        asset_path: str,
        x: float,
        y: float,
    ):
        self.name = name
        self.asset_path = asset_path
        self.x = x
        self.y = y
        self.tick_count = 0

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y

    def tick(self):
        self.tick_count += 1