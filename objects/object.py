import numpy as np
from utils.transform import Transform
from utils.material import Material, BLANK

aux = 0

class Object:
    def __init__(self, transform: Transform = None, material: Material = None):
        if transform is None:
            transform = Transform()

        if material is None:
            material = BLANK.copy()

        self.transform = transform
        self.material = material
        self.is_compound = False

    def tick(self):
        self.sendTransformToUniform()
        self.sendMaterialToUniform()

    def translate(self, x, y, z):
        self.transform.position += np.array([x, y, z])

    def scale(self, x, y, z):
        self.transform.scale *= np.array([x, y, z])

    def normalize_scale(self):
        mean = np.mean(self.transform.scale)
        self.transform.scale = np.array([mean, mean, mean], dtype=np.float32)

    def rotate(self, x, y, z):
        self.transform.rotation += np.array([x, y, z])

    def sendTransformToUniform(self):
        self.transform.setUniformTransform()

    def sendMaterialToUniform(self):
        self.material.setUniformMaterial()
