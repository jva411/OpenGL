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
        self.mouse_sensitivity = 8.0
        self.is_mouse_locked = False
        self.transform_object_mode = 'translate'

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
        self.scene.start()
        try:
            while self.keep_running:
                for event in pygame.event.get():
                    self.handle_event(event)

                self.tick()
        except KeyboardInterrupt:
            self.exit()

        self.shutdown()

    def tick(self):
        self.handle_kb_input()

        self.renderer.tick()
        self.scene.tick()

        pygame.display.flip()
        self.clock.tick(60)

    def exit(self):
        self.keep_running = False

    def shutdown(self):
        pygame.quit()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            return self.exit()

        if event.type == pygame.KEYDOWN:
            return self.handle_kb_keydown(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_button_down(event)

        if event.type == pygame.MOUSEMOTION:
            return self.handle_mouse_move(event.rel[0], event.rel[1])

        if event.type == pygame.MOUSEWHEEL:
            return self.handle_mouse_wheel(event.y)

    def handle_mouse_button_down(self, event: pygame.event.Event):
        if event.button == 2:
            return self.lock_mouse()

        if event.button == 1:
            x, y = event.pos
            if self.is_mouse_locked:
                x, y = self.width // 2, self.height // 2

            return self.scene.getObjectByPixel(x, self.height - y)

    def handle_mouse_wheel(self, wheel):
        delta_time = self.get_elapsed_time_in_seconds()
        self.movement_speed += wheel * 10 * delta_time
        self.movement_speed = max(0.2, self.movement_speed)

    def handle_mouse_move(self, delta_x, delta_y):
        buttons = pygame.mouse.get_pressed()
        if self.is_mouse_locked or buttons[2]:
            self.rotate_camera(-delta_x, -delta_y)

    def handle_kb_keydown(self, key):
        if key == pygame.K_ESCAPE:
            if self.is_mouse_locked is False:
                return self.exit()

            return self.unlock_mouse()

        if key == pygame.K_t:
            self.transform_object_mode = 'translate'
        if key == pygame.K_r:
            self.transform_object_mode = 'rotate'
        if key == pygame.K_e:
            self.transform_object_mode = 'scale'

    def handle_kb_input(self):
        keys = pygame.key.get_pressed()
        camera_translation = np.array([0.0, 0.0, 0.0])
        if keys[pygame.K_w]:
            camera_translation += np.array([0.0, 0.0, -1.0])
        if keys[pygame.K_s]:
            camera_translation += np.array([0.0, 0.0, 1.0])
        if keys[pygame.K_a]:
            camera_translation += np.array([-1.0, 0.0, 0.0])
        if keys[pygame.K_d]:
            camera_translation += np.array([1.0, 0.0, 0.0])
        if keys[pygame.K_SPACE]:
            camera_translation += np.array([0.0, 1.0, 0.0])
        if keys[pygame.K_LSHIFT]:
            camera_translation += np.array([0.0, -1.0, 0.0])

        sprint = 1.0
        if keys[pygame.K_LCTRL]:
            sprint *= 2.0
        if keys[pygame.K_LALT]:
            sprint *= 0.5

        if camera_translation.any():
            self.move_camera(*camera_translation, sprint=sprint)

        if len(self.scene.selectedObjects) > 0:
            object_translation = np.array([0.0, 0.0, 0.0])
            if keys[pygame.K_UP]:
                object_translation += np.array([0.0, 1.0, 0.0])
            if keys[pygame.K_DOWN]:
                object_translation += np.array([0.0, -1.0, 0.0])
            if keys[pygame.K_LEFT]:
                object_translation += np.array([-1.0, 0.0, 0.0])
            if keys[pygame.K_RIGHT]:
                object_translation += np.array([1.0, 0.0, 0.0])
            if keys[pygame.K_PAGEUP]:
                object_translation += np.array([0.0, 0.0, 1.0])
            if keys[pygame.K_PAGEDOWN]:
                object_translation += np.array([0.0, 0.0, -1.0])

            if object_translation.any():
                self.transform_object(*object_translation, sprint)

    def move_camera(self, right, up, forward, sprint=1.0):
        delta_time = self.get_elapsed_time_in_seconds()
        translation = np.array([right, up, forward]) * self.movement_speed * delta_time * sprint
        self.scene.camera.translate(*translation)

    def rotate_camera(self, delta_x, delta_y):
        delta_time = self.get_elapsed_time_in_seconds()
        rotation = np.array([delta_x, delta_y, 0.0]) * self.mouse_sensitivity * delta_time
        self.scene.camera.rotate(*np.radians(rotation))

    def transform_object(self, right, up, forward, sprint=1.0):
        delta_time = self.get_elapsed_time_in_seconds()
        transform = np.array([right, up, forward]) * delta_time * sprint

        match self.transform_object_mode:
            case 'translate':
                self.scene.selectedObjects[0].translate(*transform)
            case 'scale':
                self.scene.selectedObjects[0].scale(*transform)
            case 'rotate':
                rotation = (transform * 25.0)[[1, 0, 2]]
                rotation[0] *= -1.0
                self.scene.selectedObjects[0].rotate(*rotation)

    def get_elapsed_time_in_seconds(self):
        return self.clock.get_time() / 1000.0

    def lock_mouse(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.set_pos((self.width // 2, self.height // 2))
        self.is_mouse_locked = True

    def unlock_mouse(self):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.mouse.set_pos((self.width // 2, self.height // 2))
        self.is_mouse_locked = False
