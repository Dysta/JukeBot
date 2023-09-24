import unittest

from jukebot.components.requests import ShazamRequest
from jukebot.utils.logging import disable_logging


class TestShazamRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_shazam_request_success(self):
        with disable_logging():
            async with ShazamRequest(
                "https://twitter.com/LaCienegaBlvdss/status/1501975048202166283"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        result: dict = req.result

        self.assertEqual(result.get("title"), "Enya - The Humming (Official Lyric Video)")
        self.assertEqual(result.get("url"), "https://youtu.be/FOP_PPavoLA?autoplay=1")
        self.assertEqual(
            result.get("image_url"), "https://i.ytimg.com/vi/FOP_PPavoLA/maxresdefault.jpg"
        )

    async def test_shazam_request_failed(self):
        with disable_logging():
            async with ShazamRequest("https://www.instagram.com/p/Cqk4Vh0MVYo/") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
