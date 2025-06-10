from scene.camera import Camera
from objects.object import Object
from opengl.renderer import Renderer
from objects.lights.light import Light


class Scene:
    def __init__(self, camera: Camera, objects: list[Object], lights: list[Light]):
        self.camera = camera
        self.objects = objects
        self.lights = lights

    def tick(self):
        self.camera.tick()

        Renderer.renderer.bind_program(Renderer.renderer.light_program)
        self.camera.send_view_to_uniform()
        self.camera.send_projection_to_uniform()
        for light in self.lights:
            light.tick()

        Renderer.renderer.bind_program(Renderer.renderer.triangle_program)
        self.camera.send_view_to_uniform()
        self.camera.send_projection_to_uniform()
        self.camera.send_position_to_uniform()
        for light in self.lights:
            light.send_color_to_uniform()

        for obj in self.objects:
            obj.tick()
