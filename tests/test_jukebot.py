import unittest

from jukebot import __version__


class MisceleanousTest(unittest.TestCase):
    def test_version(self):
        assert __version__ == "0.1.0"
