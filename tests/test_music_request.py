import unittest

from jukebot.components import Result, ResultSet
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
            async with MusicRequest("https://www.youtube.com/watch?v=4xDzrJKXOOY") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertIn("synthwave radio 🌌 beats to chill/game to", result.get("title"))
        self.assertEqual(result.get("uploader"), "Lofi Girl")
        self.assertEqual(result.get("webpage_url"), "https://www.youtube.com/watch?v=4xDzrJKXOOY")
        self.assertIsNone(result.get("duration"))
        self.assertEqual(result.get("live_status"), "is_live")
        self.assertIsNotNone(result.get("thumbnail"))

    async def test_music_request_success_soundcloud_url(self):
        with disable_logging():
            async with MusicRequest(
                "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: dict = req.result

        self.assertEqual(result.get("title"), "Skychaser - 104.5 Sky FM (2nd Part, Slowed And Reverb)")
        self.assertEqual(result.get("uploader"), "[wstd7331]")
        self.assertEqual(
            result.get("webpage_url"),
            "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb",
        )
        self.assertEqual(round(result.get("duration")), 201)
        self.assertIsNone(result.get("thumbnail"))

    async def test_music_request_playlist_youtube_url(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0") as req:
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
            async with MusicRequest("https://soundcloud.com/dysta/sets/vanished-ep-by-evryn/s-HkTM3QuDGiW") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.PLAYLIST)

        results: list = req.result

        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 9)

        # ? SoundCloud API doesn't return any title/channel or duration
        # ? only a stream link that will be used in StreamRequest
        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 8)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 7)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 6)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 5)
        self.assertIsNotNone(result.get("url"))

        # test each result
        result = results.pop(0)
        self.assertEqual(len(results), 4)
        self.assertIsNotNone(result.get("url"))

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

    async def test_music_request_failed_youtube_query(self):
        with disable_logging():
            async with MusicRequest("khfdkjshdfglmdsjfgtlkdjsfgkjshdfkgljhdskfjghkdljfhgkldsjfhg") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.UNKNOWN)

    async def test_music_request_failed_youtube_empty_query(self):
        with disable_logging():
            async with MusicRequest("") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.UNKNOWN)

    async def test_music_request_failed_youtube_invalid_url(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/watch?v=8GW7sLrK40k") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.UNKNOWN)

    async def test_music_request_failed_soundcloud_invalid_url(self):
        with disable_logging():
            async with MusicRequest("https://soundcloud.com/dysta/loopshit-plz-dont-plz-dont") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.UNKNOWN)

    async def test_music_request_youtube_url_convert_to_result(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/watch?v=8GW6sLrK40k") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertEqual(result.title, "HOME - Resonance")
        self.assertEqual(result.channel, "Electronic Gems")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.duration, 213)
        self.assertEqual(result.fmt_duration, "3:33")
        self.assertFalse(result.live)
        self.assertIsNone(result.requester)

    async def test_music_request_youtube_query_convert_to_result(self):
        with disable_logging():
            async with MusicRequest("Home - Resonance") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertEqual(result.title, "HOME - Resonance")
        self.assertEqual(result.channel, "Electronic Gems")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=8GW6sLrK40k")
        self.assertEqual(result.duration, 213)
        self.assertEqual(result.fmt_duration, "3:33")
        self.assertFalse(result.live)
        self.assertIsNone(result.requester)

    async def test_music_request_success_soundcloud_url_convert_to_result(self):
        with disable_logging():
            async with MusicRequest(
                "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb"
            ) as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertEqual(result.title, "Skychaser - 104.5 Sky FM (2nd Part, Slowed And Reverb)")
        self.assertEqual(result.channel, "[wstd7331]")
        self.assertEqual(
            result.web_url,
            "https://soundcloud.com/wstd7331/skychaser-1045-sky-fm-2nd-part-slowed-and-reverb",
        )
        self.assertEqual(result.duration, 201)
        self.assertEqual(result.fmt_duration, "3:21")
        self.assertFalse(result.live)
        self.assertIsNone(result.requester)

    async def test_music_request_youtube_live_url_convert_to_result(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/watch?v=4xDzrJKXOOY") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertIn("synthwave radio 🌌 beats to chill/game to", result.title)
        self.assertEqual(result.channel, "Lofi Girl")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=4xDzrJKXOOY")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

    async def test_music_request_playlist_youtube_url_convert_to_resultset(self):
        with disable_logging():
            async with MusicRequest("https://www.youtube.com/playlist?list=PLjnOFoOKDEU9rzMtOaKGLABN7QhG19Nl0") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.PLAYLIST)
        self.assertTrue(isinstance(req.result, list))
        self.assertEqual(len(req.result), 8)

        results: ResultSet = ResultSet.from_result(req.result)
        self.assertEqual(len(results), 8)

        # test each result
        result: Result = results.get()
        self.assertEqual(len(results), 7)
        self.assertEqual(result.title, "Clams Casino - Water Theme")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 110)
        self.assertEqual(result.fmt_duration, "1:50")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=CCXHU3AjVPs")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 6)
        self.assertEqual(result.title, "Clams Casino - Water Theme 2")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 122)
        self.assertEqual(result.fmt_duration, "2:02")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=F-NH1cxEVz8")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 5)
        self.assertEqual(result.title, "Clams Casino - Misty")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 145)
        self.assertEqual(result.fmt_duration, "2:25")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=e2ho4sQm_sU")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 4)
        self.assertEqual(result.title, "Clams Casino - Tunnel Speed")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 138)
        self.assertEqual(result.fmt_duration, "2:18")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=x2-LawcTIVk")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 3)
        self.assertEqual(result.title, "Clams Casino - Pine")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 127)
        self.assertEqual(result.fmt_duration, "2:07")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=X1WLnqN4oPI")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 2)
        self.assertEqual(result.title, "Clams Casino - Emblem")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 110)
        self.assertEqual(result.fmt_duration, "1:50")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=41qlOmiRrLM")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 1)
        self.assertEqual(result.title, "Clams Casino - Unknown")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 81)
        self.assertEqual(result.fmt_duration, "1:21")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=4SEcDxD9QGg")
        self.assertFalse(result.live)

        result = results.get()
        self.assertEqual(len(results), 0)
        self.assertEqual(result.title, "Clams Casino - Winter Flower")
        self.assertEqual(result.channel, "Clams Casino")
        self.assertEqual(result.duration, 174)
        self.assertEqual(result.fmt_duration, "2:54")
        self.assertEqual(result.web_url, "https://www.youtube.com/watch?v=P45rOK-SlDY")
        self.assertFalse(result.live)

    async def test_music_request_playlist_soundcloud_url_convert_to_resultset(self):
        with disable_logging():
            async with MusicRequest("https://soundcloud.com/dysta/sets/vanished-ep-by-evryn/s-HkTM3QuDGiW") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.PLAYLIST)
        self.assertTrue(isinstance(req.result, list))
        self.assertEqual(len(req.result), 9)

        results: ResultSet = ResultSet.from_result(req.result)
        self.assertEqual(len(results), 9)

        # ? SoundCloud API doesn't return any title/channel or duration
        # ? only a stream link that will be used in StreamRequest
        # test each result
        result = results.get()
        self.assertEqual(len(results), 8)
        self.assertEqual(
            result.web_url,
            "https://soundcloud.com/dysta/evryn-no-more-bad-days/s-vTqs4UGlKkS",
        )
        self.assertEqual(result.title, "Evryn No More Bad Days")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 7)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-can-you-see-me/s-HDLAfyVjqfb")
        self.assertEqual(result.title, "Evryn Can You See Me")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 6)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-tears-in-the-rain/s-0b7fcsuBibx")
        self.assertEqual(result.title, "Evryn Tears In The Rain")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 5)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-reset/s-hsygXrF0aId")
        self.assertEqual(result.title, "Evryn Reset")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 4)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-colored-elements/s-9QNPeHetkTz")
        self.assertEqual(result.title, "Evryn Colored Elements")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 3)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-everything-cyclic/s-A0HhrlySRy1")
        self.assertEqual(result.title, "Evryn Everything Cyclic")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 2)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-love-you-forever/s-KL22UIGotke")
        self.assertEqual(result.title, "Evryn Love You Forever")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 1)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-promising-future/s-DDl6TFrf919")
        self.assertEqual(result.title, "Evryn Promising Future")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

        # test each result
        result = results.get()
        self.assertEqual(len(results), 0)
        self.assertEqual(result.web_url, "https://soundcloud.com/dysta/evryn-ups-and-downs/s-rcgMdEnFnBz")
        self.assertEqual(result.title, "Evryn Ups And Downs")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)

    async def test_music_request_success_soundcloud_shorted_url_convert_to_result(self):
        with disable_logging():
            async with MusicRequest("https://on.soundcloud.com/Gsdzc") as req:
                await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertEqual(result.title, "Headband Andy Vito Bad Boy")
        self.assertEqual(result.channel, "Minecraft Pukaj 009 Sk")
        self.assertEqual(
            result.web_url,
            "https://soundcloud.com/minecraft-pukaj-009-sk/headband-andy-vito-bad-boy",
        )
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)
        self.assertIsNone(result.requester)

    async def test_music_request_success_soundcloud_shorted_private_url_convert_to_result(self):
        async with MusicRequest("https://on.soundcloud.com/gA4Ca") as req:
            await req.execute()

        self.assertTrue(req.success)
        self.assertIsNotNone(req.result)
        self.assertEqual(req.type, MusicRequest.ResultType.TRACK)

        result: Result = Result(req.result)

        self.assertEqual(result.title, "Empty")
        self.assertEqual(result.channel, "Dysta")
        self.assertEqual(
            result.web_url,
            "https://soundcloud.com/dysta/empty/s-wEHdWGqgDdf",
        )
        self.assertEqual(result.duration, 0)
        self.assertEqual(result.fmt_duration, "ထ")
        self.assertTrue(result.live)
        self.assertIsNone(result.requester)
