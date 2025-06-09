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
        self.movement_speed = 1.0
        self.mouse_sensitivity = 5.0

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
            return self.exit()

        if event.type == pygame.MOUSEMOTION:
            return self.handle_mouse_move(event.rel[0], event.rel[1])

        if event.type == pygame.MOUSEWHEEL:
            return self.handle_mouse_wheel(event.y)

    def handle_mouse_wheel(self, wheel):
        delta_time = self.get_elapsed_time_in_seconds()
        self.movement_speed += wheel * 10 * delta_time
        self.movement_speed = max(0.2, self.movement_speed)

    def handle_mouse_move(self, delta_x, delta_y):
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
        delta_time = self.get_elapsed_time_in_seconds()
        translation = np.array([right, up, forward]) * self.movement_speed * delta_time
        self.scene.camera.translate(*translation)

    def rotate_camera(self, delta_x, delta_y):
        delta_time = self.get_elapsed_time_in_seconds()
        rotation = np.array([delta_x, delta_y, 0.0]) * self.mouse_sensitivity * delta_time
        self.scene.camera.rotate(*np.radians(rotation))

    def get_elapsed_time_in_seconds(self):
        return self.clock.get_time() / 1000.0
