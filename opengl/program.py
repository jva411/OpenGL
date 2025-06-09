import numpy as np
import OpenGL.GL as GL
from opengl.shaders import Shaders


class Program:
    def __init__(self, vertex_shader: str, fragment_shader: str):
        self.shaders = Shaders(vertex_shader, fragment_shader)
        self.program = GL.glCreateProgram()

        GL.glAttachShader(self.program, self.shaders.vertex_shader)
        GL.glAttachShader(self.program, self.shaders.fragment_shader)

        GL.glLinkProgram(self.program)

        GL.glDeleteShader(self.shaders.vertex_shader)
        GL.glDeleteShader(self.shaders.fragment_shader)

    def bind(self):
        GL.glUseProgram(self.program)

    def setUniformMatrix4f(self, name: str, matrix: np.ndarray):
        location = GL.glGetUniformLocation(self.program, name)
        GL.glUniformMatrix4fv(location, 1, GL.GL_FALSE, matrix)
