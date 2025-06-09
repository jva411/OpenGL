import numpy as np
from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW

class EBO:
    def __init__(self):
        self.ebo = glGenBuffers(1)

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)

    def buffer_data(self, data: np.ndarray):
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data.tobytes(), GL_STATIC_DRAW)
