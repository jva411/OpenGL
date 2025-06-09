from pathlib import Path
import numpy as np
from opengl.ebo import EBO
from opengl.texture import Texture
from opengl.vao import VAO
from opengl.vbo import VBO
from objects.object import Object
from utils.transform import Transform
from OpenGL.GL import glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT


CUBE_VERTICES = np.array([
    # [X, Y, Z], [s, t, r]

    # Back
    [[-0.5, -0.5, -0.5], [0.0, 0.0, 0.0]], # 0
    [[ 0.5, -0.5, -0.5], [1.0, 0.0, 0.0]], # 1
    [[ 0.5,  0.5, -0.5], [1.0, 1.0, 0.0]], # 2
    [[-0.5,  0.5, -0.5], [0.0, 1.0, 0.0]], # 3

    # Front
    [[-0.5, -0.5,  0.5], [0.0, 0.0, 0.0]], # 4
    [[-0.5,  0.5,  0.5], [0.0, 1.0, 0.0]], # 5
    [[ 0.5,  0.5,  0.5], [1.0, 1.0, 0.0]], # 6
    [[ 0.5, -0.5,  0.5], [1.0, 0.0, 0.0]], # 7

    # Left
    [[-0.5, -0.5, -0.5], [0.0, 0.0, 0.0]], # 8
    [[-0.5,  0.5, -0.5], [0.0, 1.0, 0.0]], # 9
    [[-0.5,  0.5,  0.5], [1.0, 1.0, 0.0]], # 10
    [[-0.5, -0.5,  0.5], [1.0, 0.0, 0.0]], # 11

    # Right
    [[ 0.5, -0.5, -0.5], [0.0, 0.0, 0.0]], # 12
    [[ 0.5, -0.5,  0.5], [1.0, 0.0, 0.0]], # 13
    [[ 0.5,  0.5,  0.5], [1.0, 1.0, 0.0]], # 14
    [[ 0.5,  0.5, -0.5], [0.0, 1.0, 0.0]], # 15

    # Top
    [[ 0.5,  0.5,  0.5], [0.0, 0.0, 0.0]], # 16
    [[-0.5,  0.5,  0.5], [1.0, 0.0, 0.0]], # 17
    [[-0.5,  0.5, -0.5], [1.0, 1.0, 0.0]], # 18
    [[ 0.5,  0.5, -0.5], [0.0, 1.0, 0.0]], # 19

    # Bottom
    [[ 0.5, -0.5,  0.5], [0.0, 0.0, 0.0]], # 20
    [[ 0.5, -0.5, -0.5], [0.0, 1.0, 0.0]], # 21
    [[-0.5, -0.5, -0.5], [1.0, 1.0, 0.0]], # 22
    [[-0.5, -0.5,  0.5], [1.0, 0.0, 0.0]], # 23
], dtype=np.float32)
CUBE_INDICES = np.array([
    [[0, 2, 1], [0, 3, 2]], # Back
    [[4, 6, 5], [4, 7, 6]], # Front
    [[8, 10, 9], [8, 11, 10]], # Left
    [[12, 14, 13], [12, 15, 14]], # Right
    [[16, 18, 17], [16, 19, 18]], # Top
    [[20, 22, 21], [20, 23, 22]], # Bottom
], dtype=np.uint32)

vao: VAO = None
vbo: VBO = None
ebo: EBO = None
texture: Texture = None

def init_cube():
    global vao, vbo, ebo, texture
    if vao is None:
        vao = VAO()
        vao.bind()

        vbo = VBO()
        vbo.bind()

        vao.addAttribute(0, 6*4, 0)
        vao.addAttribute(1, 6*4, 3*4)
        vbo.buffer_data(CUBE_VERTICES)

        ebo = EBO()
        ebo.bind()
        ebo.buffer_data(CUBE_INDICES)

        texture = Texture()
        texture.bind()
        texture.load(Path("assets/textures/box.png").absolute())

def bind_cube():
    vao.bind()
    vbo.bind()
    ebo.bind()
    texture.bind()

class Cube(Object):
    def __init__(self, transform: Transform = None):
        super().__init__(transform)
        init_cube()

    def tick(self):
        super().tick()
        bind_cube()
        glDrawElements(GL_TRIANGLES, CUBE_INDICES.size, GL_UNSIGNED_INT, None)
