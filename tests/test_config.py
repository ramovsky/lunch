import unittest
from tempfile import NamedTemporaryFile

from lunch.session import Session, SessionFinished, Config, User


class TestConfig(unittest.TestCase):

    def test_add_place(self):
        config = Config()
        config.add_place('Sisaket')
        self.assertAlmostEqual(1, len(config))
        config.add_place('Indian')
        self.assertAlmostEqual(2, len(config))
        config.add_place('Sisaket')
        self.assertAlmostEqual(2, len(config))

    def test_update_place(self):
        config = Config()
        config.add_place('Sisaket')
        self.assertAlmostEqual(.5, config.places['Sisaket'])
        config.add_place('Sisaket', .7)
        self.assertAlmostEqual(.7, config.places['Sisaket'])

    def test_save_load(self):
        file = NamedTemporaryFile().name
        config = Config(file)
        config.add_place('Sisaket')
        config.save()
        places = config.places
        config = Config(file)
        config.load()
        self.assertEqual(places, config.places)

    def test_history_crop(self):
        file = NamedTemporaryFile().name
        config = Config(file)
        for i in range(10):
            config.add_winner('Sisaket')
        config.save()
        config = Config(file)
        config.load()
        self.assertEqual(7, len(config._history))
