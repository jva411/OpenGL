import numpy as np
from utils.textures import Textures
from opengl.renderer import Renderer


class Material:
    def __init__(self, diffuse: np.ndarray = None, specular: np.ndarray = None, shininess: float = None, textures: Textures = None):
        self.diffuse = np.array(diffuse if diffuse is not None else BLANK.diffuse, dtype=np.float32)
        self.specular = np.array(specular if specular is not None else BLANK.specular, dtype=np.float32)
        self.shininess = shininess if shininess is not None else BLANK.shininess
        self.textures = textures

    def setUniformMaterial(self):
        Renderer.renderer.current_program.setUniform1f('material.shininess', self.shininess)
        if self.textures is None:
            Renderer.renderer.current_program.setUniformVec3f('material.diffuse', self.diffuse)
            Renderer.renderer.current_program.setUniformVec3f('material.specular', self.specular)
        else:
            self.textures.setUniformTextures()

    def copy(self):
        return Material(self.diffuse.copy(), self.specular.copy(), self.shininess)

BLANK = Material(
    diffuse=[1.0, 1.0, 1.0],
    specular=[0.1, 0.1, 0.1],
    shininess=1,
)
