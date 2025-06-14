import numpy as np
from opengl.renderer import Renderer
from utils.textures import Textures


class Material:
    def __init__(self, diffuse: np.ndarray, specular: np.ndarray, shininess: float, textures: Textures = None):
        self.diffuse = np.array(diffuse, dtype=np.float32)
        self.specular = np.array(specular, dtype=np.float32)
        self.shininess = shininess
        self.textures = textures

    def setUniformMaterial(self):
        Renderer.renderer.current_program.setUniform1f('material.shininess', self.shininess)
        if self.textures is not None:
            self.textures.setUniformTextures()

    def copy(self):
        return Material(self.diffuse.copy(), self.specular.copy(), self.shininess)

BLANK = Material(
    diffuse=[1.0, 1.0, 1.0],
    specular=[0.1, 0.1, 0.1],
    shininess=1,
)
