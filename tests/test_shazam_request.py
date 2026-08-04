import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from jukebot.components.requests import ShazamRequest
from jukebot.utils.logging import disable_logging


class TestShazamRequestComponent(unittest.IsolatedAsyncioTestCase):
    # @unittest.skip("not working on CI due to ffprobe not found")
    async def test_shazam_request_live_is_limited_to_30_seconds(self):
        duration: float | None = None

        async def recognize_song_patched(*, data):
            nonlocal duration
            duration = float(
                subprocess.check_output(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-show_entries",
                        "format=duration",
                        "-of",
                        "default=nw=1:nk=1",
                        str(data),
                    ],
                    text=True,
                )
            )
            return {}

        with (
            patch(
                "jukebot.components.requests.shazam_request.Shazam.recognize_song",
                side_effect=recognize_song_patched,
            ) as shazam,
            patch(
                "jukebot.components.requests.shazam_request.Serialize.full_track",
                return_value=SimpleNamespace(track=None),
            ),
        ):
            async with ShazamRequest("https://www.youtube.com/@LofiGirl/live") as req:
                await req.execute()

        shazam.assert_called_once()
        self.assertIsNotNone(duration)
        self.assertTrue(31.0 >= duration >= 29.0)
        self.assertFalse(req.success)

    # @unittest.skip("not working on CI due to ffprobe not found")
    async def test_shazam_request_success(self):
        # with disable_logging():
        async with ShazamRequest("https://twitter.com/LaCienegaBlvdss/status/1501975048202166283") as req:
            await req.execute()
            tmp_path = req._path

        self.assertTrue(req.success)
        self.assertFalse(tmp_path.exists())
        self.assertFalse(tmp_path.parent.exists())
        result: dict = req.result

        self.assertEqual(result.get("title"), "Enya - The Humming (Official Lyric Video)")
        self.assertEqual(result.get("url"), "https://youtu.be/FOP_PPavoLA?autoplay=1")
        self.assertEqual(result.get("image_url"), "https://i.ytimg.com/vi/FOP_PPavoLA/maxresdefault.jpg")

    # @unittest.skip("not working on CI due to ffprobe not found")
    async def test_shazam_request_failed(self):
        with disable_logging():
            async with ShazamRequest("https://www.instagram.com/p/Cqk4Vh0MVYo/") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
