import yaml
import random


class SessionFinished(Exception):
    pass


class Rules:
    pass


class User:

    def __init__(self, name):
        self.name = name
        self.preferences = {}

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self.name) == hash(other)


class Config:

    def __init__(self):
        self.places = {}

    def add_place(self, place, distance):
        self.places[place] = distance

    def load(self, path='places.yaml'):
        self.places = yaml.load(path)

    def save(self, path='places.yaml'):
        yaml.dump(self.places)


class Session:

    def __init__(self, config, weather_multiplier=0):
        self._weather_multiplier = weather_multiplier
        self.finished = False
        self.users = set()
        self._config = config

    def join(self, user):
        if self.finished:
            raise SessionFinished()

        self.users.add(user)

    def leave(self, user):
        if self.finished:
            raise SessionFinished()

        self.users.discard(user)

    def finish(self):
        if self.finished:
            raise SessionFinished()

        self.finished = True

        scores = {}
        for user in self.users:
            for place in self._config.places:
                scores[place] += user.preferences[place]

        total = sum(scores.values())
        threshold = random.uniform(0, total)
        acc = 0
        for place, score in scores.items():
            acc += score
            if acc >= threshold:
                self.winner = place
                break
