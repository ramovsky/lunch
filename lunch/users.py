import yaml

import lunch.config as config


class User:

    def __init__(self, id):
        self._id = id
        self._preferences =  {}

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    def __hash__(self):
        return hash(self.name.lower())

    def __eq__(self, other):
        return hash(self.name.lower()) == hash(other)

    def get_preference(self, place):
        return self._preferences.get(place, .5)

    def update(self, name, preferences):
        self._preferences = preferences
        self.name = name

    def save(self):
        with open('{}{}.yaml'.format(config.users_dir, self._id), 'w') as f:
            yaml.dump(f, dict(preferences=self._preferences, name=self.name))


def get_user(id):
    assert type(id) is str
    try:
        with open('{}{}.yaml'.format(config.users_dir, id)) as f:
            data = yaml.load(f)
            user = User(id)
            user.update(**data)
            return user

    except FileNotFoundError:
        return User(id)
