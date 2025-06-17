import numpy as np
from objects.object import Object
from opengl.renderer import Renderer
from utils.transform import Transform


WHITE = np.array([1.0, 1.0, 1.0], dtype=np.float32)


class Light(Object):
    def __init__(self, transform: Transform = None, color: np.ndarray = None, ambient: float = None, diffuse: float = None, specular: float = None):
        super().__init__(transform)

        if color is None:
            color = WHITE

        self.ambient = 1.0 if ambient is None else ambient
        self.diffuse = 1.0 if diffuse is None else diffuse
        self.specular = 1.0 if specular is None else specular

        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: np.ndarray):
        color = np.array(color, dtype=np.float32)

        self._color = color
        self.ambient_color = color * (1.0 if self.ambient is None else self.ambient)
        self.diffuse_color = color * (1.0 if self.diffuse is None else self.diffuse)
        self.specular_color = color * (1.0 if self.specular is None else self.specular)

    def tick(self):
        super().tick()
        self.sendLightToUniform()

    def sendLightToUniform(self, index: int = None):
        Renderer.renderer.current_program.setUniformVec3f('lightColor', self._color)
        if index is not None:
            Renderer.renderer.current_program.setUniformVec3f(f'lights[{index}].position', self.transform.position)
            Renderer.renderer.current_program.setUniformVec3f(f'lights[{index}].ambient', self.ambient_color)
            Renderer.renderer.current_program.setUniformVec3f(f'lights[{index}].diffuse', self.diffuse_color)
            Renderer.renderer.current_program.setUniformVec3f(f'lights[{index}].specular', self.specular_color)
