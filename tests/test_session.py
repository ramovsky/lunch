import unittest

from lunch.session import Session, SessionFinished, Config, User


class TestSession(unittest.TestCase):

    def test_finished(self):
        session = Session(Config())
        self.assertEqual(session.finished, False)
        session.finish()
        self.assertEqual(session.finished, True)
        with self.assertRaises(SessionFinished):
            session.finish()
        with self.assertRaises(SessionFinished):
            session.join(object())

    def test_join(self):
        session = Session(Config())
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
