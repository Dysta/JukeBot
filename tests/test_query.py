import unittest

from jukebot.components import Query


class TestQueryComponents(unittest.TestCase):
    def test_query(self):
        self.assertEqual("foo".upper(), "FOO")
