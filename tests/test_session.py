import unittest

from lunch.session import Session, SessionFinished, SessionEmpty, Config, User


class TestSession(unittest.TestCase):

    def test_finished(self):
        session = Session(Config())
        self.assertEqual(session.finished, False)
        session.join(User('test'))
        session.finish()
        self.assertEqual(session.finished, True)
        with self.assertRaises(SessionFinished):
            session.finish()
        with self.assertRaises(SessionFinished):
            session.join(object())
        with self.assertRaises(SessionFinished):
            session.leave(object())

    def test_empty(self):
        session = Session(object())
        with self.assertRaises(SessionEmpty):
            session.finish()

    def test_join(self):
        session = Session(object())
        session.join(User('test'))
        self.assertEqual(1, len(session.users))
        session.join(User('test1'))
        self.assertEqual(2, len(session.users))
        session.join(User('test'))
        self.assertEqual(2, len(session.users))

    def test_leave(self):
        session = Session(Config())
        session.join(User('test'))
        self.assertEqual(1, len(session.users))
        session.join(User('test1'))
        self.assertEqual(2, len(session.users))
        session.leave(User('test'))
        self.assertEqual(1, len(session.users))

    def test_winner(self):
        config = Config()
        config.add_place('Sisaket')
        config.add_place('Mall')
        session = Session(config)
        session.join(User('test'))
        session.finish()
        self.assertIn(session.winner, ('Mall', 'Sisaket'))

    def test_weather(self):
        config = Config()
        config.add_place('Sisaket', .7)
        config.add_place('Russian', .1)
        session = Session(config, .8)
        session.join(User('test'))
        weights = session._calc_weights()
        self.assertGreater(weights['Sisaket'], weights['Russian'])
        session = Session(config, .1)
        session.join(User('test'))
        weights = session._calc_weights()
        self.assertLess(weights['Sisaket'], weights['Russian'])

    def test_history_penalty(self):
        config = Config()
        config.add_place('Sisaket', .7)
        session = Session(config, .8)
        session.join(User('test'))
        old_weights = session._calc_weights()
        config.add_winner('Sisaket')
        new_weights = session._calc_weights()
        self.assertGreater(old_weights['Sisaket'], new_weights['Sisaket'])
