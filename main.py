import numpy as np
from objects.cube import Cube
from scene.scene import Scene
from scene.camera import Camera
from scene.window import Window
from objects.triangle import Triangle


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

    t0 = Triangle()
    t0.scale(0.5, 0.5, 0.0)
    t0.translate(0.5, 0.5, 0.5)

    t1 = Triangle()
    t1.scale(0.5, 0.5, 0.0)
    t1.translate(0.0, 0.0, 0.5)

    t2 = Triangle()
    t2.scale(0.5, 0.5, 0.0)
    t2.translate(-0.5, -0.5, 0.5)

    triangles = [t0, t1, t2]

    c0 = Cube()
    c0.translate(0.5, 0.5, 0.5)

    cubes = [c0]
    # cubes = []
    objects = [*triangles, *cubes]

    scene = Scene(camera, objects)

    window.load_scene(scene)
    window.main_loop()

if __name__ == "__main__":
    main()
