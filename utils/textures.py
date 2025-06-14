from opengl.texture import Texture
from opengl.renderer import Renderer


class Textures:
    def __init__(self, diffuse: str, specular: str):
        self.diffuse = Texture()
        self.diffuse.bind(0)
        self.diffuse.load(diffuse)

        self.specular = Texture()
        self.specular.bind(1)
        self.specular.load(specular)

    def setUniformTextures(self):
        Renderer.renderer.current_program.setUniform1i('material.diffuse', 0)
        Renderer.renderer.current_program.setUniform1i('material.specular', 1)
