from objects.object import Object
from scene.camera import Camera


class Scene:
    def __init__(self, camera: Camera, objects: list[Object]):
        self.camera = camera
        self.objects = objects

    def tick(self):
        self.camera.tick()
        for obj in self.objects:
            obj.tick()
