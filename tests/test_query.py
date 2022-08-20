import unittest

from jukebot.components import Query, Song


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
        qry: Query = Query("lofi hip hop radio")
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
