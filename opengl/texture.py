import cv2
import OpenGL.GL as GL


class Texture:
    def __init__(self):
        self.texture = GL.glGenTextures(1)

    def bind(self, index: int):
        GL.glActiveTexture(GL.GL_TEXTURE0 + index)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

    def load(self, filename):
        image = cv2.imread(filename)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            image.shape[1],
            image.shape[0],
            0,
            GL.GL_BGR,
            GL.GL_UNSIGNED_BYTE,
            image
        )
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
