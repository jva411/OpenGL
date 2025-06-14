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
        GL.glEnable(GL.GL_STENCIL_TEST)

        GL.glClearColor(0.53, 0.81, 0.92, 1.0)

        self.triangle_program = Program(open('assets/shaders/triangle/shader.vert', 'r').read(), open('assets/shaders/triangle/shader.frag', 'r').read())
        self.light_program = Program(open('assets/shaders/light/shader.vert', 'r').read(), open('assets/shaders/light/shader.frag', 'r').read())
        self.stencil_program = Program(open('assets/shaders/triangle/shader.vert', 'r').read(), open('assets/shaders/triangle/outline.frag', 'r').read())

    def bind_program(self, program: Program):
        self.current_program = program
        program.bind()

    def tick(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)

    def enableHighlight():
        GL.glStencilFunc(GL.GL_NOTEQUAL, 1, 0xFF)
        GL.glStencilMask(0x00)
        GL.glDisable(GL.GL_DEPTH_TEST)

    def disableHighlight():
        GL.glStencilMask(0xFF)
        GL.glStencilFunc(GL.GL_ALWAYS, 0, 0xFF)
        GL.glEnable(GL.GL_DEPTH_TEST)
