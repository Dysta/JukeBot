import unittest

from jukebot.components import Query, Result, ResultSet, Song
from jukebot.utils.logging import disable_logging


class TestQueryComponents(unittest.IsolatedAsyncioTestCase):
    async def test_query_to_song_from_url(self):
        with disable_logging():
            qry: Query = Query("https://www.youtube.com/watch?v=hpwnjXrPxtM")
            await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.(qry)
        self.assertEqual(song.title, "tech house mix | vascoprod")
        self.assertEqual(song.duration, 1824)
        self.assertEqual(song.fmt_duration, "30:24")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=hpwnjXrPxtM")
        self.assertEqual(song.channel, "vascoprod")
        self.assertFalse(song.live)

    async def test_query_to_song_from_url_live(self):
        with disable_logging():
            qry: Query = Query("https://www.youtube.com/watch?v=rUxyKA_-grg")
            await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.(qry)
        self.assertIn("lofi hip hop radio 💤 - beats to sleep/chill", song.title)
        self.assertEqual(song.duration, 0)
        self.assertEqual(song.fmt_duration, "ထ")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=rUxyKA_-grg")
        self.assertEqual(song.channel, "Lofi Girl")
        self.assertTrue(song.live)

    async def test_query_to_song_from_str(self):
        with disable_logging():
            qry: Query = Query("home resonance")
            await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.(qry)
        self.assertEqual(song.title, "HOME - Resonance")
        self.assertEqual(song.duration, 213)
        self.assertEqual(song.fmt_duration, "3:33")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(song.channel, "Electronic Gems")
        self.assertFalse(song.live)

    async def test_query_to_song_from_str_live(self):
        with disable_logging():
            qry: Query = Query("lofi hip hop radio - beats to relax/study to")
            await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.(qry)
        self.assertIn("lofi hip hop radio 📚 - beats to relax/study to", song.title)
        self.assertEqual(song.duration, 0)
        self.assertEqual(song.fmt_duration, "ထ")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=jfKfPfyJRdk")
        self.assertEqual(song.channel, "Lofi Girl")
        self.assertTrue(song.live)

    async def test_query_to_playlist_from_url(self):
        with disable_logging():
            qry: Query = Query(
                "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0"
            )
            await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.PLAYLIST)
        self.assertEqual(len(qry.results), 8)

        results: ResultSet = ResultSet.(qry)
        result: Result = None

        # test each result
        result = results.get()
        self.assertEqual(len(results), 7)
        self.assertEqual(result.title, "Clams Casino - Water Theme")
        self.assertEqual(result.duration, 110)
        self.assertEqual(result.fmt_duration, "1:50")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 6)
        self.assertEqual(result.title, "Clams Casino - Water Theme 2")
        self.assertEqual(result.duration, 122)
        self.assertEqual(result.fmt_duration, "2:02")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 5)
        self.assertEqual(result.title, "Clams Casino - Misty")
        self.assertEqual(result.duration, 144)
        self.assertEqual(result.fmt_duration, "2:24")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 4)
        self.assertEqual(result.title, "Clams Casino - Tunnel Speed")
        self.assertEqual(result.duration, 138)
        self.assertEqual(result.fmt_duration, "2:18")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 3)
        self.assertEqual(result.title, "Clams Casino - Pine")
        self.assertEqual(result.duration, 127)
        self.assertEqual(result.fmt_duration, "2:07")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 2)
        self.assertEqual(result.title, "Clams Casino - Emblem")
        self.assertEqual(result.duration, 110)
        self.assertEqual(result.fmt_duration, "1:50")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 1)
        self.assertEqual(result.title, "Clams Casino - Unknown")
        self.assertEqual(result.duration, 81)
        self.assertEqual(result.fmt_duration, "1:21")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 0)
        self.assertEqual(result.title, "Clams Casino - Winter Flower")
        self.assertEqual(result.duration, 173)
        self.assertEqual(result.fmt_duration, "2:53")
        self.assertIsNotNone(result.web_url)
        self.assertEqual(result.channel, "Clams Casino")
        self.assertFalse(result.live)
