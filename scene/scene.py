import time
from math import sin
from scene.camera import Camera
from objects.object import Object
from opengl.renderer import Renderer
from objects.lights.light import Light

class Scene:
    def __init__(self, camera: Camera, objects: list[Object], lights: list[Light]):
        self.camera = camera
        self.objects = objects
        self.lights = lights

    def start(self):
        self.start_time = time.time()

    def tick(self):
        self.elapsed_time = time.time() - self.start_time
        self.camera.tick()

        Renderer.renderer.bind_program(Renderer.renderer.light_program)
        self.camera.send_view_to_uniform()
        self.camera.send_projection_to_uniform()
        for light in self.lights:
            # light.color = [sin(self.elapsed_time * 0.17), sin(self.elapsed_time * 0.37), sin(self.elapsed_time * 0.41)]
            light.tick()

        Renderer.renderer.bind_program(Renderer.renderer.triangle_program)
        self.camera.send_view_to_uniform()
        self.camera.send_projection_to_uniform()
        for light in self.lights:
            light.sendLightToUniform()

        for obj in self.objects:
            obj.tick()
