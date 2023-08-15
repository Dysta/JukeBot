import asyncio
import unittest
from typing import Tuple

from jukebot.components.requests import MusicRequest
from jukebot.utils import converter
from jukebot.utils.logging import disable_logging


class TestRadios(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls._radios: dict = converter.radios_yaml_to_dict()

    async def _inner(self, music_request: MusicRequest) -> Tuple[str, bool]:
        await music_request.execute()
        return music_request.query, music_request.success

    async def test_radio_available(self):
        with disable_logging():
            for k, v in self._radios.items():
                ops: list = []
                for link in v:
                    mr: MusicRequest = MusicRequest(link)
                    ops.append(self._inner(music_request=mr))
                res = await asyncio.gather(*ops, return_exceptions=True)
                for l, r in res:
                    with self.subTest(f"Test link {l} for radio {k}"):
                        self.assertTrue(r)
