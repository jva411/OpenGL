from pathlib import Path
import numpy as np
from opengl.vao import VAO
from opengl.vbo import VBO
from opengl.ebo import EBO
from objects.object import Object
from opengl.texture import Texture
from utils.material import Material
from utils.transform import Transform
from OpenGL.GL import glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT


CUBE_VERTICES = np.array([
    # [[X,  Y,    Z,       Nx,   Ny,   Nz,     S,   T ]]
    [-0.5, -0.5, -0.5,     0.0,  0.0, -1.0,    0.0, 0.0], # 0   Back
    [ 0.5, -0.5, -0.5,     0.0,  0.0, -1.0,    1.0, 0.0], # 1
    [ 0.5,  0.5, -0.5,     0.0,  0.0, -1.0,    1.0, 1.0], # 2
    [-0.5,  0.5, -0.5,     0.0,  0.0, -1.0,    0.0, 1.0], # 3

    [-0.5, -0.5,  0.5,     0.0,  0.0,  1.0,    0.0, 0.0], # 4   Front
    [-0.5,  0.5,  0.5,     0.0,  0.0,  1.0,    0.0, 1.0], # 5
    [ 0.5,  0.5,  0.5,     0.0,  0.0,  1.0,    1.0, 1.0], # 6
    [ 0.5, -0.5,  0.5,     0.0,  0.0,  1.0,    1.0, 0.0], # 7

    [-0.5, -0.5, -0.5,    -1.0,  0.0,  0.0,    0.0, 0.0], # 8   Left
    [-0.5,  0.5, -0.5,    -1.0,  0.0,  0.0,    0.0, 1.0], # 9
    [-0.5,  0.5,  0.5,    -1.0,  0.0,  0.0,    1.0, 1.0], # 10
    [-0.5, -0.5,  0.5,    -1.0,  0.0,  0.0,    1.0, 0.0], # 11

    [ 0.5, -0.5, -0.5,     1.0,  0.0,  0.0,    0.0, 0.0], # 12  Right
    [ 0.5, -0.5,  0.5,     1.0,  0.0,  0.0,    1.0, 0.0], # 13
    [ 0.5,  0.5,  0.5,     1.0,  0.0,  0.0,    1.0, 1.0], # 14
    [ 0.5,  0.5, -0.5,     1.0,  0.0,  0.0,    0.0, 1.0], # 15

    [ 0.5,  0.5,  0.5,     0.0,  1.0,  0.0,    0.0, 0.0], # 16  Top
    [-0.5,  0.5,  0.5,     0.0,  1.0,  0.0,    1.0, 0.0], # 17
    [-0.5,  0.5, -0.5,     0.0,  1.0,  0.0,    1.0, 1.0], # 18
    [ 0.5,  0.5, -0.5,     0.0,  1.0,  0.0,    0.0, 1.0], # 19

    [ 0.5, -0.5,  0.5,     0.0, -1.0,  0.0,    1.0, 0.0], # 20  Bottom
    [ 0.5, -0.5, -0.5,     0.0, -1.0,  0.0,    1.0, 1.0], # 21
    [-0.5, -0.5, -0.5,     0.0, -1.0,  0.0,    0.0, 1.0], # 22
    [-0.5, -0.5,  0.5,     0.0, -1.0,  0.0,    0.0, 0.0], # 23
], dtype=np.float32)
CUBE_INDICES = np.array([
    [[ 0,  2,  1], [ 0,  3,  2]], # Back
    [[ 4,  6,  5], [ 4,  7,  6]], # Front
    [[ 8, 10,  9], [ 8, 11, 10]], # Left
    [[12, 14, 13], [12, 15, 14]], # Right
    [[16, 18, 17], [16, 19, 18]], # Top
    [[20, 22, 21], [20, 23, 22]], # Bottom
], dtype=np.uint32)

# 8 numbers of float32
CUBE_STRIDE = 8 * 4

#             X,Y,Z,  Nx,Ny,Nz  S,T
#             0       3         6
CUBE_SKIPS = [0,      3*4,      6*4]

vao: VAO = None
vbo: VBO = None
ebo: EBO = None
texture0: Texture = None
texture1: Texture = None

def init_cube():
    global vao, vbo, ebo, texture0, texture1
    if vao is None:
        vao = VAO()
        vao.bind()

        vbo = VBO()
        vbo.bind()

        for index, skip in enumerate(CUBE_SKIPS):
            vao.addAttribute(index, CUBE_STRIDE, skip)

        vbo.buffer_data(CUBE_VERTICES)

        ebo = EBO()
        ebo.bind()
        ebo.buffer_data(CUBE_INDICES)

        texture0 = Texture()
        texture0.bind(0)
        texture0.load(Path("assets/textures/steel_framed_box.png").absolute())

        texture1 = Texture()
        texture1.bind(1)
        texture1.load(Path("assets/textures/steel_framed_box_frame.png").absolute())


def bind_cube():
    vao.bind()
    vbo.bind()
    ebo.bind()
    texture0.bind(0)
    texture1.bind(1)

class Cube(Object):
    def __init__(self, transform: Transform = None, material: Material = None):
        super().__init__(transform, material)
        init_cube()

    def tick(self):
        super().tick()
        bind_cube()
        glDrawElements(GL_TRIANGLES, CUBE_INDICES.size, GL_UNSIGNED_INT, None)
