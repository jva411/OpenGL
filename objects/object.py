import numpy as np
from objects.transform import Transform
from opengl.renderer import Renderer

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
        Renderer.renderer.program.setUniformMatrix4f('model', self.transform.get_model().T)

        global aux
        if aux < 2:
            aux += 1
            print(self.transform.get_model().T)
        # Renderer.renderer.program.setUniformMatrix4f('model', np.array([
        #     [0.5, 0.0, 0.0, 0.0],
        #     [0.0, 0.5, 0.0, 0.0],
        #     [0.0, 0.0, 1.0, 0.0],
        #     [0.5, 0., 0.0, 1.0],
        # ], dtype=np.float32))
