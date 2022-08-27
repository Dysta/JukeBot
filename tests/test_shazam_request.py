import unittest

from jukebot.components.requests import ShazamRequest


class TestShazamRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_shazam_request_success(self):
        async with ShazamRequest(
            "https://twitter.com/thibaultbrock/status/1499800398244335624"
        ) as req:
            await req.execute()

        self.assertTrue(req.success)
        result: dict = req.result

        self.assertEqual(
            result.get("title"),
            "We Came As Romans - Black Hole  (Live from St. Andrew's Hall Detroit)",
        )
        self.assertEqual(result.get("url"), "https://youtu.be/4VPFMTSR8SU?autoplay=1")
        self.assertEqual(
            result.get("image_url"), "https://i.ytimg.com/vi/4VPFMTSR8SU/maxresdefault.jpg"
        )

    async def test_shazam_request_failed(self):
        async with ShazamRequest("https://www.instagram.com/p/Ce67Z4gJPuv/") as req:
            await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
