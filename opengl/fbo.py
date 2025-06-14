from OpenGL import GL


class FBO:
    def __init__(self):
        self.fbo = GL.glGenFramebuffers(1)
        self.texture = GL.glGenTextures(1)
        self.rbo = GL.glGenRenderbuffers(1)

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, 800, 600, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, None)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture, 0)

        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self.rbo)
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH24_STENCIL8, 800, 600)
        GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_RENDERBUFFER, self.rbo)

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('Framebuffer is not complete!')

    def unbind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, 0)
