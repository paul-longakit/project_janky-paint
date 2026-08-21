import pygame
import sys
import math

# ==========================================
# 1. DOMAIN LAYER (Core Data Models)
# ==========================================
class CanvasConfig:
    def __init__(self, width=800, height=600, fps=30, bg_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.fps = fps
        self.bg_color = bg_color

class Entity:
    def __init__(self, name, image_path, start_x, start_y, behavior=None):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.behavior = behavior
        self.tick_count = 0 # Keeps track of time for this entity
        
        # Load image and keep transparency (works with transparent PNGs)
        self.image = pygame.image.load(image_path).con  vert_alpha()

# ==========================================
# 2. USE CASE LAYER (Live Behaviors)
# ==========================================
class Behaviors:
    @staticmethod
    def janky_slide_right(entity):
        # Moves right. If it goes off-screen, it wraps back around!
        entity.x += 3
        if entity.x > 850: 
            entity.x = -100

    @staticmethod
    def chaotic_jiggle(entity):
        # Trembles in place using a sine wave math trick
        entity.tick_count += 1
        entity.y += math.sin(entity.tick_count) * 2

    @staticmethod
    def static(entity):
        # Does absolutely nothing.
        pass

# ==========================================
# 3. INFRASTRUCTURE LAYER (Live Display)
# ==========================================
class LiveSimulator:
    def __init__(self, config: CanvasConfig):
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Live Lore Box")
        self.clock = pygame.time.Clock()
        self.entities = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def run(self):
        print("Starting live simulation... Press ESC or close the window to exit.")
        running = True
        
        while running:
            # 1. Handle user closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # 2. Clear the screen (paint it white)
            self.screen.fill(self.config.bg_color)

            # 3. Update logic and draw each entity
            for entity in self.entities:
                # Run the behavior logic if it exists
                if entity.behavior:
                    entity.behavior(entity)
                
                # Draw the image to the screen
                self.screen.blit(entity.image, (entity.x, entity.y))

            # 4. Refresh the display and wait for the next frame
            pygame.display.flip()
            self.clock.tick(self.config.fps)

        pygame.quit()
        sys.exit()

# ==========================================
# 4. YOUR DAILY SCRIPT (The Workflow)
# ==========================================
if __name__ == "__main__":
    # Create the live window (Standard YouTube aspect ratio sized down)
    config = CanvasConfig(width=800, height=600, fps=30)
    sim = LiveSimulator(config)

    # To run this, you need "gort.png" and "toaster.png" in the same folder.
    # Day 1:
    sim.add_entity(Entity("Gort", "gort.png", start_x=350, start_y=400, behavior=Behaviors.static))
    
    # Day 2:
    sim.add_entity(Entity("Toaster", "toaster.png", start_x=0, start_y=100, behavior=Behaviors.janky_slide_right))

    # Run the live box!
    sim.run()