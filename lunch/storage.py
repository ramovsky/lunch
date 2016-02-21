import yaml


class YamlBackend:

    def __init__(self, path='.', name='fort'):
        self.restaurant = {}
        self.history = []
        self._path = '{}/{}.yaml'.format(path, name)
        self._loaded = False

    def __enter__(self):
        self._load()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            self._save()

    def _load(self):
        if self._loaded:
            return
        try:
            with open(self._path) as f:
                data = yaml.load(f)
        except FileNotFoundError:
            data = dict(restaurants={}, history=[])

        self.restaurants = data['restaurants']
        self.history = data['history'][-7:]
        self._loaded = True

    def _save(self):
        data = dict(restaurants=self.restaurants, history=self.history)
        with open(self._path, 'w') as f:
            yaml.dump(data, f)


class TeamStorage:

    def __init__(self, team_name='fort'):
        self._backend = YamlBackend(name=team_name)

    def __len__(self):
        return len(self.restaurants)

    def add_restaurant(self, name, distance=.5):
        with self._backend as bc:
            bc.restaurants[name] = distance

    def delete_restaurant(self, name):
        with self._backend as bc:
            bc.restaurants.pop(name, None)

    def get_resstaurans(self):
        with self._backend as bc:
            return [dict(name=k, distance=v)
                    for k, v in bc.restaurants.items()]

    def add_winner(self, restaurant):
        with self._backend as bc:
            bc.history.insert(0, restaurant)

    def get_recent(self, restaurant):
        try:
            index = self._history.index(restaurant)
            if index < 8:
                return 8 - index
        except ValueError:
            pass

        return 1
