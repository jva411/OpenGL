import numpy as np
from opengl.renderer import Renderer
from utils.transform import Transform

aux = 0

class Object:
    def __init__(self, transform: Transform = None):
        if transform is None:
            transform = Transform()

        self.transform = transform

    def tick(self):
        self.updateModel()

    def translate(self, x, y, z):
        self.transform.position += np.array([x, y, z])

    def scale(self, x, y, z):
        self.transform.scale *= np.array([x, y, z])

    def updateModel(self):
        Renderer.renderer.triangle_program.setUniformMatrix4f('model', self.transform.get_model().T)
