import time
import numpy as np
from OpenGL import GL
from opengl.fbo import FBO
from scene.camera import Camera
from objects.object import Object
from opengl.renderer import Renderer
from objects.lights.light import Light

class Scene:
    def __init__(self, camera: Camera, objects: list[Object], lights: list[Light]):
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.fbo: FBO = None
        self.selectedObjects: list[Object] = []

    def start(self):
        self.start_time = time.time()

    def tick(self):
        self.elapsed_time = time.time() - self.start_time
        self.camera.tick()

        if len(self.selectedObjects) > 0:
            self.renderHighlightedObjects()

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

    def renderHighlightedObjects(self):
        Renderer.enableHighlight()
        Renderer.renderer.bind_program(Renderer.renderer.stencil_program)
        self.camera.setCameraUniforms()
        scale = 1.1
        for obj in self.selectedObjects:
            temp = obj.transform.scale.copy()
            obj.transform.scale *= scale
            obj.tick()
            obj.transform.scale = temp
        Renderer.disableHighlight()

    def renderSelectionFramebuffer(self):
        if self.fbo is None:
            self.fbo = FBO()

        self.fbo.bind()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        Renderer.renderer.bind_program(Renderer.renderer.selection_program)
        self.camera.setCameraUniforms()
        for index, obj in enumerate(self.objects):
            color = self.idToColor(index+1)
            Renderer.renderer.current_program.setUniformVec3f('codeColor', color)
            obj.tick()

    def idToColor(self, id):
        R = (id & 0x000000FF) >> 0
        G = (id & 0x0000FF00) >> 8
        B = (id & 0x00FF0000) >> 16
        return np.array([R, G, B], dtype=np.float32) / 255.0

    def colorToId(self, color):
        R = color[0]
        G = color[1]
        B = color[2]
        return R | (G << 8) | (B << 16)

    def getObjectByPixel(self, x, y):
        self.renderSelectionFramebuffer()
        self.fbo.bind()
        bPixels: bytes = GL.glReadPixels(x, y, 1, 1, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        [R, G, B] = bPixels
        id = self.colorToId([R, G, B])
        GL.glClearColor(0.53, 0.81, 0.92, 1.0)
        self.fbo.unbind()

        if id == 0:
            self.selectedObjects = []
        else:
            self.selectedObjects = [self.objects[id-1]]
