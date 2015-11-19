import yaml
import random
from collections import defaultdict


class SessionFinished(Exception):
    pass


class SessionEmpty(Exception):
    pass


class User:

    def __init__(self, name):
        self.name = name
        self._preferences = {}

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self.name) == hash(other)

    def get_preference(self, place):
        return self._preferences.get(place, .5)


class Config:

    def __init__(self, path='places.yaml'):
        self.places = {}
        self._path = path
        self._history = []

    def __len__(self):
        return len(self.places)

    def add_place(self, place, distance=.5):
        self.places[place] = distance

    def load(self):
        with open(self._path) as f:
            self.places = yaml.load(f)

    def save(self):
        with open(self._path, 'w') as f:
            yaml.dump(self.places, f)


class Session:

    def __init__(self, config, weather=0.8):
        # 1 -- great weather, 0 -- aweful
        self._weather = 1 - weather
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
        if not self.users:
            raise SessionEmpty()

        if self.finished:
            raise SessionFinished()

        self.finished = True
        scores = self._calc_weights()
        self.winner = self._get_winner(scores)

    def _calc_weights(self):
        weights = defaultdict(float)
        for user in self.users:
            for place in self._config.places:
                weights[place] += user.get_preference(place)

        # if weather is nice further restaurant prefered and vice versa
        for place, distance in self._config.places.items():
            weights[place] *= .1 + abs(self._weather - distance)

        # penalty for restaurants visited recently
        return weights

    def _get_winner(self, scores):
        # weighted random
        total = sum(scores.values())
        threshold = random.uniform(0, total)
        acc = 0
        for place, score in scores.items():
            acc += score
            if acc >= threshold:
                return place
