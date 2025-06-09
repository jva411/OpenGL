import numpy as np
from opengl.ebo import EBO
from opengl.vao import VAO
from opengl.vbo import VBO
from objects.object import Object
from utils.transform import Transform
from OpenGL.GL import glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT


CUBE_VERTICES = np.array([
    [-0.5, -0.5, -0.5],
    [ 0.5, -0.5, -0.5],
    [ 0.5,  0.5, -0.5],
    [-0.5,  0.5, -0.5],
    [-0.5, -0.5,  0.5],
    [ 0.5, -0.5,  0.5],
    [ 0.5,  0.5,  0.5],
    [-0.5,  0.5,  0.5],
], dtype=np.float32)
CUBE_INDICES = np.array([
    # Back
    [2, 1, 0],
    [3, 2, 0],

    # Front
    [4, 5, 6],
    [4, 6, 7],

    # Left
    [7, 3, 4],
    [3, 0, 4],

    # Right
    [5, 1, 6],
    [1, 2, 6],

    # Top
    [2, 3, 6],
    [3, 7, 6],

    # Bottom
    [4, 0, 5],
    [0, 1, 5],
], dtype=np.uint32)

vao: VAO = None
vbo: VBO = None
ebo: EBO = None

def init_cube():
    global vao, vbo, ebo
    if vao is None:
        vao = VAO()
        vao.bind()

        vbo = VBO()
        vbo.bind()

        vao.addAttribute(0)
        vbo.buffer_data(CUBE_VERTICES)

        ebo = EBO()
        ebo.bind()
        ebo.buffer_data(CUBE_INDICES)

def bind_cube():
    vao.bind()
    vbo.bind()
    ebo.bind()

class Cube(Object):
    def __init__(self, transform: Transform = None):
        super().__init__(transform)
        init_cube()

    def tick(self):
        super().tick()
        bind_cube()
        glDrawElements(GL_TRIANGLES, CUBE_INDICES.size, GL_UNSIGNED_INT, None)
