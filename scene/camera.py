import numpy as np
from utils import vector
from opengl.renderer import Renderer


class Camera:
    def __init__(self, position: np.ndarray, direction: np.ndarray, up: np.ndarray, fov: float, aspect: float, near: float, far: float):
        self.position = position
        self.direction = vector.normalize(direction)
        self.up = vector.normalize(up)
        self.right = np.cross(self.direction, self.up)
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

        self.rotated_right = self.right
        self.rotated_up = self.up
        self.rotated_direction = self.direction

    def get_view_matrix(self):
        P = self.position
        R, U, D = self.rotated_right, self.rotated_up, self.rotated_direction

        return np.array([
            [ R[0],  R[1],  R[2], -P.dot(R)],
            [ U[0],  U[1],  U[2], -P.dot(U)],
            [-D[0], -D[1], -D[2],  P.dot(D)],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def get_perspective_matrix(self):
        f = 1.0 / np.tan(np.radians(self.fov) * 0.5)
        a = f / self.aspect
        inv_length = 1.0 / (self.near - self.far)
        b = (self.near + self.far) * inv_length
        c = (2.0 * self.near * self.far) * inv_length

        return np.array([
            [a, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, b, c],
            [0.0, 0.0, -1.0, 0.0],
        ], dtype=np.float32)

    def translate(self, right, up, forward):
        translate_right = right * vector.normalize(np.array([self.rotated_right[0], 0.0, self.rotated_right[2]]))
        translate_up = up * np.array([0.0, 1.0, 0.0])
        translate_forward = forward * vector.normalize(np.array([self.rotated_direction[0], 0.0, self.rotated_direction[2]]))

        self.position += translate_right + translate_up - translate_forward

    def rotate(self, x_rad=0.0, y_rad=0.0, z_rad=0.0):
        self.rotation += np.array([x_rad, y_rad, z_rad])

        U, R, D = self.up, self.right, self.direction

        yaw = vector.get_rotation_matrix(U, self.rotation[0])
        pitch = vector.get_rotation_matrix(R, self.rotation[1])
        roll = vector.get_rotation_matrix(D, self.rotation[2])

        rotation_matrix = yaw @ pitch @ roll

        R = rotation_matrix @ R
        U = rotation_matrix @ U
        D = rotation_matrix @ D

        self.rotated_right = R
        self.rotated_up = U
        self.rotated_direction = D

    def send_view_to_uniform(self):
        Renderer.renderer.program.setUniformMatrix4f('view', self.get_view_matrix().T)

    def send_projection_to_uniform(self):
        Renderer.renderer.program.setUniformMatrix4f('projection', self.get_perspective_matrix().T)

    def tick(self):
        self.send_view_to_uniform()
        self.send_projection_to_uniform()
