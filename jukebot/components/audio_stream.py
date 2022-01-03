from nextcord import FFmpegOpusAudio


class AudioStream(FFmpegOpusAudio):
    def __init__(self, source: str, seek: int = 0):
        extra = f" -ss {seek}s" if seek else ""
        super(AudioStream, self).__init__(
            source,
            before_options=_PlayerOption.FFMPEG_BEFORE_OPTIONS,  # "-nostdin",
            options=f"{_PlayerOption.FFMPEG_OPTIONS}{extra}",
        )
        self._progress: int = 0
        self._offset: int = seek

    def read(self) -> bytes:
        data = super().read()
        if data:
            self._progress += 1
        return data

    @property
    def progress(self) -> int:
        # 20ms
        return int(self._progress * 0.02) + self._offset


class _PlayerOption:

    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
