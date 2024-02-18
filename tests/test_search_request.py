import unittest

from jukebot.components import ResultSet
from jukebot.components.requests import SearchRequest
from jukebot.utils.logging import disable_logging


class TestSearchRequestComponent(unittest.IsolatedAsyncioTestCase):
    async def test_search_request_url_song_youtube_raise_exception(self):
        with disable_logging():
            with self.assertRaises(ValueError):
                async with SearchRequest(
                    "https://www.youtube.com/watch?v=YZ2WJ1krQss",
                    SearchRequest.Engine.Youtube,
                ) as req:
                    await req()

    async def test_search_request_url_song_Soundcloud_raise_exception(self):
        with disable_logging():
            with self.assertRaises(ValueError):
                async with SearchRequest(
                    "https://SoundCloud.com/gee_baller/playboi-carti-cult-classic",
                    SearchRequest.Engine.SoundCloud,
                ) as req:
                    await req()

    async def test_search_request_url_playlist_youtube_raise_exception(self):
        with disable_logging():
            with self.assertRaises(ValueError):
                async with SearchRequest(
                    "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0",
                    SearchRequest.Engine.Youtube,
                ) as req:
                    await req()

    async def test_search_request_url_playlist_Soundcloud_raise_exception(self):
        with disable_logging():
            with self.assertRaises(ValueError):
                async with SearchRequest(
                    "https://SoundCloud.com/dysta/sets/breakcore", SearchRequest.Engine.SoundCloud
                ) as req:
                    await req()

    async def test_search_request_query_song_youtube_success_using_engine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", SearchRequest.Engine.Youtube) as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_youtube_success_convert_resultset_using_engine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", SearchRequest.Engine.Youtube) as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

        set = ResultSet.from_result(result)

        self.assertLessEqual(len(set), 10)

    async def test_search_request_query_song_Soundcloud_success_using_engine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", SearchRequest.Engine.SoundCloud) as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_Soundcloud_convert_resultset_using_engine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", SearchRequest.Engine.SoundCloud) as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

        set = ResultSet.from_result(result)

        self.assertLessEqual(len(set), 10)

    async def test_search_request_query_song_youtube_success_using_strengine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", "ytsearch10:") as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_youtube_convert_resultset_using_strengine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", "ytsearch10:") as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

        set = ResultSet.from_result(result)

        self.assertLessEqual(len(set), 10)

    async def test_search_request_query_song_Soundcloud_success_using_strengine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", "scsearch10:") as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

    async def test_search_request_query_song_Soundcloud_convert_resultset_using_strengine(self):
        with disable_logging():
            async with SearchRequest("Slowdive - sleep", "scsearch10:") as req:
                await req()

        self.assertTrue(req.result)
        self.assertIsNotNone(req.result)
        self.assertIsInstance(req.result, list)

        result: list = req.result

        self.assertLessEqual(len(result), 10)

        set = ResultSet.from_result(result)

        self.assertLessEqual(len(set), 10)
