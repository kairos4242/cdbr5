class Clock:

    # simple clock, pygame clock get_ticks() looks like it returns ms and not actual frames elapsed, this will return current game frame for replay purposes
    def __init__(self):
        self._ticks = 0

    def tick(self):
        self._ticks += 1

    def untick(self):
        self._ticks -= 1

    def get_ticks(self):
        return self._ticks