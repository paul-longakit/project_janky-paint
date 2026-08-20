class PygameRenderer:

    def __init__(self):
        self.images = {}

    def load_asset(self, path):
        if path not in self.images:
            self.images[path] = pygame.image.load(
                path
            ).convert_alpha()

        return self.images[path]

    def render_entity(self, screen, entity):
        image = self.load_asset(entity.asset_path)

        screen.blit(
            image,
            (entity.x, entity.y),
        )