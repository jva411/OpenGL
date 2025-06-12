import numpy as np
from opengl.renderer import Renderer


class Material:
    def __init__(self, diffuse: np.ndarray, specular: np.ndarray, shininess: float):
        self.diffuse = np.array(diffuse, dtype=np.float32)
        self.specular = np.array(specular, dtype=np.float32)
        self.shininess = shininess

    def setUniformMaterial(self):
        # Renderer.renderer.current_program.setUniformVec3f('material.diffuse', self.diffuse)
        # Renderer.renderer.current_program.setUniformVec3f('material.specular', self.specular)
        Renderer.renderer.current_program.setUniform1i('material.diffuse', 0)
        Renderer.renderer.current_program.setUniform1i('material.specular', 1)
        Renderer.renderer.current_program.setUniform1f('material.shininess', self.shininess)

    def copy(self):
        return Material(self.diffuse.copy(), self.specular.copy(), self.shininess)

BLANK = Material(
    diffuse=[1.0, 1.0, 1.0],
    specular=[0.1, 0.1, 0.1],
    shininess=1,
)
