import os
import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from jukebot.components.requests import ShazamRequest
from jukebot.utils.logging import disable_logging


class TestShazamRequestComponent(unittest.IsolatedAsyncioTestCase):
    @unittest.skipIf(os.getenv("CI"), "requires ffprobe and network access")
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
                "jukebot.components.requests.shazam_request.Shazam.recognize",
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

    @unittest.skipIf(os.getenv("CI"), "requires ffprobe and network access")
    async def test_shazam_request_success(self):
        # with disable_logging():
        async with ShazamRequest("https://twitter.com/LaCienegaBlvdss/status/1501975048202166283") as req:
            await req.execute()
            tmp_path = req._path

        self.assertTrue(req.success)
        self.assertFalse(tmp_path.exists())
        self.assertFalse(tmp_path.parent.exists())
        result: dict = req.result

        self.assertEqual(result.get("title"), "The Humming...")
        self.assertEqual(result.get("author"), "Enya")
        self.assertEqual(result.get("url"), "https://music.apple.com/gb/album/the-humming/1043622490")
        self.assertTrue(result.get("image_url"))
        self.assertNotIn("Shazam", result.get("links"))
        self.assertEqual(result["links"]["Apple Music"], "https://music.apple.com/gb/album/the-humming/1043622490")
        self.assertEqual(result["links"]["Spotify"], "https://open.spotify.com/search/The%20Humming...%20Enya")

    @unittest.skipIf(os.getenv("CI"), "requires ffprobe and network access")
    async def test_shazam_request_failed(self):
        with disable_logging():
            async with ShazamRequest("https://www.instagram.com/p/Cqk4Vh0MVYo/") as req:
                await req.execute()

        self.assertFalse(req.success)
        self.assertIsNone(req.result)
