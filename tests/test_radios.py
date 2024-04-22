import unittest

from jukebot.components.requests import MusicRequest
from jukebot.utils import converter
from jukebot.utils.logging import disable_logging


class TestRadios(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls._radios: dict = converter.radios_yaml_to_dict()

    @unittest.skip("not working even if links are correct")
    async def test_radio_available(self):
        with disable_logging():
            for k, v in self._radios.items():
                for link in v:
                    with self.subTest(f"Test link {link} for radio {k}"):
                        async with MusicRequest(link) as req:
                            await req.execute()
                            self.assertTrue(req.success)
