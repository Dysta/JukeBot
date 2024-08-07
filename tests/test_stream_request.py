import unittest

from jukebot.components import Song
from jukebot.components.requests import StreamRequest
from jukebot.utils.logging import disable_logging


class TestStreamRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_stream_request_success_youtube(self):
        with disable_logging():
            async with StreamRequest("https://www.youtube.com/watch?v=8GW6sLrK40k") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, dict)

        result: dict = req.result

        self.assertEqual(result.get("title"), "HOME - Resonance")
        self.assertEqual(result.get("uploader"), "Electronic Gems")
        self.assertEqual(result.get("webpage_url"), "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.get("duration"), 213)

        self.assertIsNotNone(result.get("thumbnail", None))
        self.assertIsNotNone(result.get("url", None))

        self.assertFalse(result.get("is_live"))

    async def test_stream_request_success_soundcloud(self):
        with disable_logging():
            async with StreamRequest(
                "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, dict)

        result: dict = req.result

        self.assertEqual(result.get("title"), "Skychaser - 104.5 Sky FM (2nd Part, Slowed And Reverb)")
        self.assertEqual(result.get("uploader"), "[wstd7331]")
        self.assertEqual(
            result.get("webpage_url"),
            "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb",
        )
        self.assertEqual(round(result.get("duration")), 201)

        self.assertIsNotNone(result.get("thumbnail", None))
        self.assertIsNotNone(result.get("url", None))

    async def test_stream_request_playlist_youtube(self):
        with disable_logging():
            async with StreamRequest("https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0") as req:
                await req.execute()
        self.assertFalse(req.success)
        self.assertIsNone(req.result)

    async def test_stream_request_playlist_soundcloud(self):
        with disable_logging():
            async with StreamRequest("https://soundcloud.com/dysta/sets/breakcore") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)

    async def test_stream_request_success_youtube_query(self):
        with disable_logging():
            async with StreamRequest("home resonance") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)

    async def test_stream_request_success_youtube_convert_to_song(self):
        with disable_logging():
            async with StreamRequest("https://www.youtube.com/watch?v=8GW6sLrK40k") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, dict)

        result: Song = Song(req.result)

        self.assertEqual(result.title, "HOME - Resonance")
        self.assertEqual(result.channel, "Electronic Gems")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.duration, 213)
        self.assertEqual(result.fmt_duration, "3:33")

        self.assertIsNotNone(result.thumbnail)
        self.assertIsNotNone(result.stream_url)

        self.assertFalse(result.live)

    async def test_stream_request_success_youtube_live_convert_to_song(self):
        with disable_logging():
            async with StreamRequest("https://www.youtube.com/watch?v=4xDzrJKXOOY") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, dict)

        result: Song = Song(req.result)

        self.assertIn("synthwave radio 🌌 - beats to chill/game to", result.title)
        self.assertEqual(result.channel, "Lofi Girl")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=4xDzrJKXOOY")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")

        self.assertIsNotNone(result.thumbnail)
        self.assertIsNotNone(result.stream_url)

        self.assertTrue(result.live)

    async def test_stream_request_success_soundcloud_convert_to_song(self):
        with disable_logging():
            async with StreamRequest(
                "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, dict)

        result: Song = Song(req.result)

        self.assertEqual(result.title, "Skychaser - 104.5 Sky FM (2nd Part, Slowed And Reverb)")
        self.assertEqual(result.channel, "[wstd7331]")
        self.assertEqual(
            result.web_url,
            "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb",
        )
        self.assertEqual(result.duration, 201)
        self.assertEqual(result.fmt_duration, "3:21")

        self.assertIsNotNone(result.thumbnail)
        self.assertIsNotNone(result.stream_url)
