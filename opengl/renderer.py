import pygame
from OpenGL import GL
from opengl.program import Program


class Renderer:
    renderer = None

    def __init__(self):
        Renderer.renderer = self
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glEnable(GL.GL_CULL_FACE)

        GL.glClearColor(0.2, 0.3, 0.3, 1.0)

        self.program = Program(open('assets/shaders/shader.vert', 'r').read(), open('assets/shaders/shader.frag', 'r').read())
        self.program.bind()

    def tick(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
