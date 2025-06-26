from opengl.texture import Texture
from opengl.renderer import Renderer


class Textures:
    def __init__(self, diffuse: str = None, specular: str = None):
        self.diffuse = Texture()
        if diffuse is not None:
            self.loadDiffuse(diffuse)

        self.specular = Texture()
        if specular is not None:
            self.loadSpecular(specular)

    def loadDiffuse(self, diffuse: str):
        self.diffuse.bind(0)
        self.diffuse.load(diffuse)

    def loadSpecular(self, specular: str):
            self.specular.bind(1)
            self.specular.load(specular)

    def setUniformTextures(self):
        self.diffuse.bind(0)
        self.specular.bind(1)
        Renderer.renderer.current_program.setUniform1i('material.diffuse', 0)
        Renderer.renderer.current_program.setUniform1i('material.specular', 1)
