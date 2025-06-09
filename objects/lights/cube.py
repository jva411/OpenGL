import numpy as np
import OpenGL.GL as GL
from opengl.ebo import EBO
from opengl.vao import VAO
from opengl.vbo import VBO
from utils.transform import Transform
from objects.lights.light import Light
from objects.cube import CUBE_INDICES, CUBE_VERTICES


LIGHT_CUBE_VERTICES = CUBE_VERTICES[:, 0]

vao: VAO = None
vbo: VBO = None
ebo: EBO = None

def init_light_cube():
    global vao, vbo, ebo
    if vao is None:
        vao = VAO()
        vao.bind()

        vbo = VBO()
        vbo.bind()

        vao.addAttribute(0, 3*4, 0)
        vbo.buffer_data(LIGHT_CUBE_VERTICES)

        ebo = EBO()
        ebo.bind()
        ebo.buffer_data(CUBE_INDICES)

def bind_light_cube():
    vao.bind()
    vbo.bind()
    ebo.bind()

class LightCube(Light):
    def __init__(self, transform: Transform = None, color: np.ndarray = None):
        super().__init__(transform, color)
        init_light_cube()

    def tick(self):
        super().tick()
        bind_light_cube()
        GL.glDrawElements(GL.GL_TRIANGLES, CUBE_INDICES.size, GL.GL_UNSIGNED_INT, None)
