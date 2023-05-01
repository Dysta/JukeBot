import unittest

from jukebot.components.requests import MusicRequest
from jukebot.utils.logging import disable_logging


class TestMusicRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_music_request_success_youtube_url(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/watch?v=8GW6sLrK40k") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertEqual(result.get("title"), "HOME - Resonance")
        self.assertEqual(result.get("uploader"), "Electronic Gems")
        self.assertEqual(result.get("webpage_url"), "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.get("duration"), 213)
        self.assertEqual(result.get("live_status"), "not_live")
        self.assertIsNotNone(result.get("thumbnail"))

    async def test_music_request_success_youtube_live_url(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/watch?v=MVPTGNGiI-4") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertIn("synthwave radio 🌌 - beats to chill/game to", result.get("title"))
        self.assertEqual(result.get("uploader"), "Lofi Girl")
        self.assertEqual(result.get("webpage_url"), "https://www.youtube.com/watch?v=MVPTGNGiI-4")
        self.assertIsNone(result.get("duration"))
        self.assertEqual(result.get("live_status"), "is_live")
        self.assertIsNotNone(result.get("thumbnail"))

    async def test_music_request_success_soundcloud_url(self):
        with disable_logging():
            async with MusicRequest(
                "https://soundcloud.com/gee_baller/playboi-carti-cult-classic"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertEqual(result.get("title"), "Playboi Carti – Cult Classic")
        self.assertEqual(result.get("uploader"), "Gee Baller")
        self.assertEqual(
            result.get("webpage_url"),
            "https://soundcloud.com/gee_baller/playboi-carti-cult-classic",
        )
        self.assertEqual(round(result.get("duration")), 118)
        self.assertIsNone(result.get("thumbnail"))

    async def test_music_request_playlist_youtube_url(self):
        with disable_logging():
            async with MusicRequest(
                "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.PLAYLIST)

        results: list = req.result

        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 8)

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 7)
        self.assertEqual(result.get("title"), "Clams Casino - Water Theme")
        self.assertEqual(result.get("duration"), 110)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 6)
        self.assertEqual(result.get("title"), "Clams Casino - Water Theme 2")
        self.assertEqual(result.get("duration"), 122)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 5)
        self.assertEqual(result.get("title"), "Clams Casino - Misty")
        self.assertEqual(result.get("duration"), 145)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 4)
        self.assertEqual(result.get("title"), "Clams Casino - Tunnel Speed")
        self.assertEqual(result.get("duration"), 138)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 3)
        self.assertEqual(result.get("title"), "Clams Casino - Pine")
        self.assertEqual(result.get("duration"), 127)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 2)
        self.assertEqual(result.get("title"), "Clams Casino - Emblem")
        self.assertEqual(result.get("duration"), 110)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 1)
        self.assertEqual(result.get("title"), "Clams Casino - Unknown")
        self.assertEqual(result.get("duration"), 81)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

        result = results.pop(0)
        self.assertEqual(len(results), 0)
        self.assertEqual(result.get("title"), "Clams Casino - Winter Flower")
        self.assertEqual(result.get("duration"), 174)
        self.assertIsNotNone(result.get("url"))
        self.assertEqual(result.get("channel"), "Clams Casino")

    async def test_music_request_playlist_soundcloud_url(self):
        with disable_logging():
            async with MusicRequest("https://soundcloud.com/dysta/sets/breakcore") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.PLAYLIST)

        results: list = req.result

        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 4)

        # ? SoundCloud API doesn't return any title/channel or duration
        # ? only a stream link that will be used in StreamRequest
        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 3)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 2)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 0)
        self.assertIsNotNone(result.get("url"))

    async def test_music_request_success_youtube_query(self):
        with disable_logging():
            async with MusicRequest("Home - Resonance") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertEqual(result.get("title"), "HOME - Resonance")
        self.assertEqual(result.get("channel"), "Electronic Gems")
        self.assertEqual(result.get("url"), "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.get("duration"), 213)
