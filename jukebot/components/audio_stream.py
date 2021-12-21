import platform
import sys
from io import SEEK_CUR

from nextcord import FFmpegPCMAudio
from nextcord.opus import Encoder as OpusEncoder


class AudioStream(FFmpegPCMAudio):
    def __init__(self, source: str):
        super(AudioStream, self).__init__(
            source,
            executable=_PlayerOption.FFMPEG_EXECUTABLE[platform.system()],
            pipe=False,
            stderr=sys.stdout,  # None,  # subprocess.PIPE
            before_options=_PlayerOption.FFMPEG_BEFORE_OPTIONS,  # "-nostdin",
            options=_PlayerOption.FFMPEG_OPTIONS,
        )
        self._progress: int = 0

    def read(self) -> bytes:
        ret = self._stdout.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b""
        self._progress += 1
        return ret

    def seek(self, sec: int = 1):
        self._stdout.seek(sec, SEEK_CUR)

    @property
    def progress(self) -> int:
        # 20ms
        return int(self._progress * 0.02)


class _PlayerOption:
    FFMPEG_EXECUTABLE = {"Linux": "./bin/ffmpeg", "Windows": "./bin/ffmpeg.exe"}

    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
