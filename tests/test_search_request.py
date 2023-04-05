import unittest

from jukebot.components import ResultSet
from jukebot.components.requests import SearchRequest


class TestSearchRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_search_request_url_song_youtube_raise_exception(self):
        with self.assertRaises(ValueError):
            async with SearchRequest(
                "https://www.youtube.com/watch?v=YZ2WJ1krQss", "ytsearch10:"
            ) as req:
                await req.execute()

    async def test_search_request_url_song_soundcloud_raise_exception(self):
        with self.assertRaises(ValueError):
            async with SearchRequest(
                "https://soundcloud.com/gee_baller/playboi-carti-cult-classic", "scsearch10:"
            ) as req:
                await req.execute()

    async def test_search_request_url_playlist_youtube_raise_exception(self):
        with self.assertRaises(ValueError):
            async with SearchRequest(
                "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0",
                "ytsearch10:",
            ) as req:
                await req.execute()

    async def test_search_request_url_playlist_soundcloud_raise_exception(self):
        with self.assertRaises(ValueError):
            async with SearchRequest(
                "https://soundcloud.com/dysta/sets/breakcore", "scsearch10:"
            ) as req:
                await req.execute()

    async def test_search_request_query_song_youtube_success(self):
        async with SearchRequest("Slowdive - sleep", "ytsearch10:") as req:
            await req.execute()

        self.assertFalse(req._process)

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_soundcloud_success(self):
        async with SearchRequest("Slowdive - sleep", "scsearch10:") as req:
            await req.execute()

        self.assertTrue(req._process)

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_soundcloud_convert_resultset(self):
        async with SearchRequest("Slowdive - sleep", "scsearch10:") as req:
            await req.execute()

        self.assertTrue(req._process)

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

        set = ResultSet.from_result(result)

        self.assertLessEqual(len(set), 10)
