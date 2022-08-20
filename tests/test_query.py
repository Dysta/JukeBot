import unittest

from jukebot.components import Query, Result, ResultSet, Song


class TestQueryComponents(unittest.IsolatedAsyncioTestCase):
    async def test_query_to_song_from_url(self):
        qry: Query = Query("https://www.youtube.com/watch?v=hpwnjXrPxtM")
        await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.from_query(qry)
        self.assertEqual(song.title, "tech house mix | vascoprod")
        self.assertEqual(song.duration, 1824)
        self.assertEqual(song.fmt_duration, "30:24")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=hpwnjXrPxtM")
        self.assertEqual(song.channel, "vascoprod")
        self.assertFalse(song.live)

    async def test_query_to_song_from_str(self):
        qry: Query = Query("lofi hip hop radio - beats to relax/study to")
        await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.TRACK)

        song: Song = Song.from_query(qry)
        self.assertEqual(song.title, "lofi hip hop radio - beats to relax/study to")
        self.assertEqual(song.duration, 0)
        self.assertEqual(song.fmt_duration, "ထ")
        self.assertEqual(song.web_url, "https://www.youtube.com/watch?v=jfKfPfyJRdk")
        self.assertEqual(song.channel, "Lofi Girl")
        self.assertTrue(song.live)

    async def test_query_to_playlist_from_url(self):
        qry: Query = Query(
            "https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0"
        )
        await qry.process()
        self.assertTrue(qry.success)
        self.assertEqual(qry.type, Query.Type.PLAYLIST)
        self.assertEqual(len(qry.results), 8)

        results: ResultSet = ResultSet.from_query(qry)
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
