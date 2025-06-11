import numpy as np
from opengl.renderer import Renderer


class Material:
    def __init__(self, ambient: np.ndarray, diffuse: np.ndarray, specular: np.ndarray, shininess: float):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def setUniformMaterial(self):
        Renderer.renderer.current_program.setUniformVec3f('material.ambient', self.ambient)
        Renderer.renderer.current_program.setUniformVec3f('material.diffuse', self.diffuse)
        Renderer.renderer.current_program.setUniformVec3f('material.specular', self.specular)
        Renderer.renderer.current_program.setUniform1f('material.shininess', self.shininess)

    def copy(self):
        return Material(self.ambient.copy(), self.diffuse.copy(), self.specular.copy(), self.shininess)

BLANK = Material(
    ambient=np.array([1.0, 1.0, 1.0]),
    diffuse=np.array([1.0, 1.0, 1.0]),
    specular=np.array([0.1, 0.1, 0.1]),
    shininess=1,
)
