import pygame
import numpy as np
from scene.scene import Scene
from opengl.renderer import Renderer


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title
        self.keep_running = True

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
        try:
            while self.keep_running:
                for event in pygame.event.get():
                    self.handle_event(event)

                self.handle_kb_input()

                self.tick()
        except KeyboardInterrupt:
            self.exit()

        self.shutdown()

    def tick(self):
        self.renderer.tick()
        self.scene.tick()

        pygame.display.flip()
        self.clock.tick(60)

    def exit(self):
        self.keep_running = False

    def shutdown(self):
        pygame.quit()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.exit()
            return

        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_input(event.rel[0], event.rel[1])

    def handle_mouse_input(self, delta_x, delta_y):
        buttons = pygame.mouse.get_pressed()
        if buttons[2]:
            self.rotate_camera(-delta_x, -delta_y)

    def handle_kb_input(self):
        keys = pygame.key.get_pressed()
        translation = np.array([0.0, 0.0, 0.0])
        if keys[pygame.K_w]:
            translation += np.array([0.0, 0.0, -1.0])
        if keys[pygame.K_s]:
            translation += np.array([0.0, 0.0, 1.0])
        if keys[pygame.K_a]:
            translation += np.array([-1.0, 0.0, 0.0])
        if keys[pygame.K_d]:
            translation += np.array([1.0, 0.0, 0.0])
        if keys[pygame.K_SPACE]:
            translation += np.array([0.0, 1.0, 0.0])
        if keys[pygame.K_LSHIFT]:
            translation += np.array([0.0, -1.0, 0.0])

        self.move_camera(*translation)

    def move_camera(self, right, up, forward):
        speed = 1.0
        elapsed_time_in_seconds = self.clock.get_time() / 1000.0
        translation = np.array([right, up, forward]) * speed * elapsed_time_in_seconds
        self.scene.camera.translate(*translation)

    def rotate_camera(self, delta_x, delta_y):
        speed = 5.0
        elapsed_time_in_seconds = self.clock.get_time() / 1000.0
        rotation = np.array([delta_x, delta_y, 0.0]) * speed * elapsed_time_in_seconds
        self.scene.camera.rotate(*np.radians(rotation))
