class SessionFinished(Exception):
    pass


class Session:

    def __init__(self, name, weather_multiplier=0):
        self._name = name
        self._weather_multiplier = weather_multiplier
        self._finished = False

    def join(self, name, preferences):
        if self._finished:
            raise SessionFinished()

    def finish(self):
        self._finished = True
