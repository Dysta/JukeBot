import unittest

from jukebot.components.requests import MusicRequest


class TestMusicRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_music_request_success_youtube(self):
        async with MusicRequest("https://www.youtube.com/watch?v=YZ2WJ1krQss") as req:
            await req.execute()

        self.assertTrue(req.success)
        result: dict = req.result

        self.assertEqual(result.get("title"), "Righteous")
        self.assertEqual(result.get("uploader"), "Mo Beats - Topic")
        self.assertEqual(result.get("webpage_url"), "https://www.youtube.com/watch?v=YZ2WJ1krQss")
        self.assertEqual(result.get("duration"), 164)

        self.assertIsNotNone(result.get("thumbnail", None))
        self.assertIsNotNone(result.get("url", None))

        self.assertFalse(result.get("is_live"))

    async def test_music_request_success_soundcloud(self):
        async with MusicRequest(
            "https://soundcloud.com/gee_baller/playboi-carti-cult-classic"
        ) as req:
            await req.execute()

        self.assertTrue(req.success)
        result: dict = req.result

        self.assertEqual(result.get("title"), "Playboi Carti – Cult Classic")
        self.assertEqual(result.get("uploader"), "Gee Baller")
        self.assertEqual(
            result.get("webpage_url"),
            "https://soundcloud.com/gee_baller/playboi-carti-cult-classic",
        )
        self.assertEqual(round(result.get("duration")), 118)

        self.assertIsNotNone(result.get("thumbnail", None))
        self.assertIsNotNone(result.get("url", None))

    async def test_music_request_playlist_youtube(self):
        async with MusicRequest(
            "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0"
        ) as req:
            await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)

    async def test_music_request_playlist_soundcloud(self):
        async with MusicRequest("https://soundcloud.com/dysta/sets/breakcore") as req:
            await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
