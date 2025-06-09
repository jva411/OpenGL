from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER


class Shaders:
    def __init__(self, vertex_shader: str, fragment_shader: str):
        self.vertex_shader = shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
