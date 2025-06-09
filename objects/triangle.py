import numpy as np
from opengl.vao import VAO
from objects.object import Object
from utils.transform import Transform
from OpenGL.GL import glDrawArrays, GL_TRIANGLES

from opengl.vbo import VBO

TRIANGLE = np.array([
    [-0.5, -0.5, 0.0],
    [ 0.5, -0.5, 0.0],
    [ 0.0,  0.5, 0.0],
], dtype=np.float32)

vao: VAO = None
vbo: VBO = None

def init_triangle():
    global vao, vbo
    if vao is None:
        vao = VAO()
        vao.bind()

        vbo = VBO()
        vbo.bind()

        vao.addAttribute(0)
        vbo.buffer_data(TRIANGLE)

def bind_triangle():
    vao.bind()
    vbo.bind()

class Triangle(Object):
    def __init__(self, transform: Transform = None):
        super().__init__(transform)
        init_triangle()

    def tick(self):
        super().tick()
        bind_triangle()
        glDrawArrays(GL_TRIANGLES, 0, 3)
