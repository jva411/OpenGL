from scene.scene import Scene
from scene.window import Window
from objects.triangle import Triangle


def main():
    aspect_ratio = 16 / 9
    width = 800
    height = int(width / aspect_ratio)
    window = Window(width, height, "OpenGL")
    window.open()

    t0 = Triangle()
    t0.scale(0.5, 0.5, 1.0)
    t0.translate(0.5, 0.5, 0.0)

    t1 = Triangle()
    t1.scale(0.5, 0.5, 1.0)

    t2 = Triangle()
    t2.scale(0.5, 0.5, 1.0)
    t2.translate(-0.5, -0.5, 0.0)

    triangles = [t0, t1, t2]
    objects = [*triangles]
    scene = Scene(objects)

    window.load_scene(scene)
    window.main_loop()

if __name__ == "__main__":
    main()
