import numpy as np
from objects.object import Object
from opengl.renderer import Renderer
from utils.transform import Transform


class Light(Object):
    def __init__(self, transform: Transform = None, color: np.ndarray = None):
        super().__init__(transform)

        if color is None:
            color = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        self.color = color

    def tick(self):
        super().tick()
        self.send_color_to_uniform()

    def send_color_to_uniform(self):
        Renderer.renderer.current_program.setUniformVec3f('lightColor', self.color)
        Renderer.renderer.current_program.setUniformVec3f('lightPosition', self.transform.position)
