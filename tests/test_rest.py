from .base import BaseTestCase


class TestSession(BaseTestCase):

    def test_get_main(self):
        print(self.run(self.communicate('/')))
