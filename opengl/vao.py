import ctypes
from OpenGL.GL import glGenVertexArrays, glBindVertexArray, glVertexAttribPointer, glEnableVertexAttribArray, GL_FLOAT, GL_FALSE


class VAO:
    def __init__(self):
        # self.vao = glGenVertexArrays(1)
        self.vao = glGenVertexArrays(1)

    def bind(self):
        glBindVertexArray(self.vao)

    def addAttribute(self, index: int):
        size = 4 * 3
        skip = size * index

        glVertexAttribPointer(
            index,
            3,
            GL_FLOAT,
            GL_FALSE,
            size,
            ctypes.c_void_p(skip),
        )
        glEnableVertexAttribArray(index)
