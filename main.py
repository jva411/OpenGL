import os
if os.name == "posix":
    os.environ["PYOPENGL_PLATFORM"] = "glx"

import numpy as np
from objects.cube import Cube
from objects.lights.cube import LightCube
from scene.scene import Scene
from scene.camera import Camera
from scene.window import Window
from utils.material import Material


def main():
    aspect_ratio = 16 / 9
    width = 800
    height = int(width / aspect_ratio)
    window = Window(width, height, "OpenGL")
    window.open()

    camera = Camera(
        position=np.array([0.0, 0.0, 3.0], dtype=np.float32),
        direction=np.array([0.0, 0.0, -1.0], dtype=np.float32),
        up=np.array([0.0, 1.0, 0.0], dtype=np.float32),
        fov=45.0,
        aspect=aspect_ratio,
        near=0.1,
        far=100.0,
    )

    c0 = Cube(
        material=Material(
            ambient=np.array([1.0, 0.5, 0.31]),
            diffuse=np.array([1.0, 0.5, 0.31]),
            specular=np.array([0.5, 0.5, 0.5]),
            shininess=32,
        ),
    )
    c0.translate(0.0, 0.0, -1.0)

    cubes = [c0]

    l0 = LightCube(color=[1.0, 1.0, 1.0], ambient=0.2, diffuse=0.5)
    l0.translate(1.5, 1.0, 0.5)
    l0.scale(0.3, 0.3, 0.3)

    objects = [*cubes]
    lights = [l0]
    scene = Scene(camera, objects, lights)

    window.load_scene(scene)
    window.main_loop()

if __name__ == "__main__":
    main()
