import numpy as np
from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, GL_ARRAY_BUFFER, GL_STATIC_DRAW

class VBO:
    def __init__(self):
        self.vbo = glGenBuffers(1)

    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def buffer_data(self, data: np.ndarray):
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data.tobytes(), GL_STATIC_DRAW)
