import numpy as np
import OpenGL.GL as GL
from opengl.vao import VAO
from opengl.vbo import VBO
from opengl.ebo import EBO
from objects.object import Object
from utils.material import Material
from utils.transform import Transform

class Mesh(Object):
    def __init__(self, vertices: np.ndarray, indices: np.ndarray, transform: Transform = None, material: Material = None):
        super().__init__(transform, material)
        self.vertices = vertices
        self.indices = indices
        self.setup_mesh()

    def setup_mesh(self):
        self.vao = VAO()
        self.vao.bind()

        self.vbo = VBO()
        self.vbo.bind()
        self.vbo.buffer_data(self.vertices)

        self.ebo = EBO()
        self.ebo.bind()
        self.ebo.buffer_data(self.indices)

        # Posição
        self.vao.addAttribute(0, 8 * 4, 0)
        # Normais
        self.vao.addAttribute(1, 8 * 4, 3 * 4)
        # Coordenadas de Textura
        self.vao.addAttribute(2, 8 * 4, 6 * 4)

    def tick(self):
        super().tick()
        self.vao.bind()
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)
