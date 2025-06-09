from objects.object import Object


class Scene:
    def __init__(self, objects: list[Object]):
        self.objects = objects

    def tick(self):
        for obj in self.objects:
            obj.tick()
