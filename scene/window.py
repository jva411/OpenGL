import pygame

from opengl.renderer import Renderer
from scene.scene import Scene


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title

    def open(self):
        pygame.display.init()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.OPENGL)
        self.renderer = Renderer()

        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    def load_scene(self, scene: Scene):
        self.scene = scene

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.tick()

    def tick(self):
        self.renderer.program.program
        self.renderer.tick()
        self.scene.tick()

        pygame.display.flip()
        self.clock.tick(60)
