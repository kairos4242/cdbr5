from game_objects.GameObjects import GameObject


class ObjectCreation:

    def __init__(self, obj: "GameObject", timestamp: int):
        self.object = obj
        self.timestamp = timestamp

        print(f"A(n) {str(type(obj))} was created at {timestamp}")