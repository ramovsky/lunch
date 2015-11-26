import unittest

from lunch.users import User, UserFactory


class TestUser(unittest.TestCase):

    def test_factory(self):
        factory = UserFactory()
        user = factory.get_user('asdfsad')
        self.assertEqual(type(user), User)
