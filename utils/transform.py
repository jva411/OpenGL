import numpy as np
from math import cos, sin
from opengl.renderer import Renderer


class Transform:
    def __init__(self, position: np.ndarray = None, rotation: np.ndarray = None, scale: np.ndarray = None):
        if position is None:
            position = np.array([0.0, 0.0, 0.0], dtype=np.float32)

        if rotation is None:
            rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32)

        if scale is None:
            scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)

        self.position = position
        self.rotation = rotation
        self.scale = scale

    def get_model(self):
        model = np.identity(4)

        # Translation
        translate_mat = np.eye(4)
        translate_mat[:3, 3] = self.position

        rx, ry, rz = np.radians(self.rotation)

        # Rotation around X axis (pitch)
        rx_mat = np.eye(4)
        rx_mat[1, 1] =  cos(rx)
        rx_mat[1, 2] = -sin(rx)
        rx_mat[2, 1] =  sin(rx)
        rx_mat[2, 2] =  cos(rx)

        # Rotation around Y axis (yaw)
        ry_mat = np.eye(4)
        ry_mat[0, 0] =  cos(ry)
        ry_mat[0, 2] =  sin(ry)
        ry_mat[2, 0] = -sin(ry)
        ry_mat[2, 2] =  cos(ry)

        # Rotation around Z axis (roll)
        rz_mat = np.eye(4)
        rz_mat[0, 0] =  cos(rz)
        rz_mat[0, 1] = -sin(rz)
        rz_mat[1, 0] =  sin(rz)
        rz_mat[1, 1] =  cos(rz)

        rotation_mat = rz_mat @ ry_mat @ rx_mat

        # Apply scale
        scale_mat = np.eye(4)
        np.fill_diagonal(scale_mat[:3, :3], self.scale)

        model = translate_mat @ rotation_mat @ scale_mat
        return model

    def setUniformTransform(self):
        Renderer.renderer.current_program.setUniformMatrix4f('model', self.get_model().T)
