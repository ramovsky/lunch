import yaml
import random
from collections import defaultdict


class SessionFinished(Exception):
    pass


class SessionEmpty(Exception):
    pass


class Config:

    def __init__(self, path='config.yaml'):
        self.places = {}
        self._path = path
        self._history = []

    def __len__(self):
        return len(self.places)

    def add_place(self, place, distance=.5):
        self.places[place] = distance

    def add_winner(self, place):
        self._history.insert(0, place)

    def get_recent(self, place):
        try:
            index = self._history.index(place)
            if index < 8:
                return 8 - index
        except ValueError:
            pass

        return 1

    def load(self):
        with open(self._path) as f:
            data = yaml.load(f)
        self.places = data['places']
        self._history = data['history'][-7:]

    def save(self):
        data = dict(places=self.places, history=self._history)
        with open(self._path, 'w') as f:
            yaml.dump(data, f)


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
        self._config.add_winner(self.winner)

    def _calc_weights(self):
        weights = defaultdict(float)
        for user in self.users:
            for place in self._config.places:
                weights[place] += user.get_preference(place)

        for place, distance in self._config.places.items():
            # if weather is nice further restaurant prefered and vice versa
            weights[place] *= .1 + (self._weather - distance)**2

            # penalty for restaurants visited recently
            weights[place] *= 1/self._config.get_recent(place)

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
