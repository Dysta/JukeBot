import os
import unittest

import yaml

from jukebot.components.requests import MusicRequest
from jukebot.utils.logging import disable_logging


class TestRadios(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        with open("./data/radios.yaml", "r") as f:
            cls._radios = yaml.safe_load(f)

    @unittest.skipIf(os.getenv("CI"), ("not working even if links are correct"))
    async def test_radio_available(self):
        with disable_logging():
            for k, v in self._radios.items():
                for link in v:
                    with self.subTest(f"Test link {link} for radio {k}"):
                        async with MusicRequest(link) as req:
                            await req.execute()
                            self.assertTrue(req.success)
