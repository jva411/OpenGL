import time
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

        # self.renderHighlightedObjects(self.objects)

        Renderer.renderer.bind_program(Renderer.renderer.light_program)
        self.camera.setCameraUniforms()
        for light in self.lights:
            light.tick()

        Renderer.renderer.bind_program(Renderer.renderer.triangle_program)
        self.camera.setCameraUniforms()
        for light in self.lights:
            light.sendLightToUniform()

        for obj in self.objects:
            obj.tick()

    def renderHighlightedObjects(self, highlighted_objects: list[Object]):
        Renderer.enableHighlight()
        Renderer.renderer.bind_program(Renderer.renderer.stencil_program)
        self.camera.setCameraUniforms()
        scale = 1.1
        for obj in highlighted_objects:
            temp = obj.transform.scale.copy()
            obj.transform.scale *= scale
            obj.tick()
            obj.transform.scale = temp
        Renderer.disableHighlight()
