from nextcord import FFmpegOpusAudio

_MISSING = object()


class AudioStream(FFmpegOpusAudio):
    def __init__(
        self, source: str, before_options: str = _MISSING, options: str = _MISSING
    ):
        if before_options is _MISSING:
            before_options = _PlayerOption.FFMPEG_BEFORE_OPTIONS
        if options is _MISSING:
            options = _PlayerOption.FFMPEG_OPTIONS

        super(AudioStream, self).__init__(
            source,
            before_options=before_options,  # "-nostdin",
            options=options,
        )
        self._progress: int = 0

    def read(self) -> bytes:
        data = super().read()
        if data:
            self._progress += 1
        return data

    @property
    def progress(self) -> int:
        # 20ms
        return int(self._progress * 0.02)


class _PlayerOption:
    FFMPEG_BEFORE_OPTIONS = " ".join(
        ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 3", "-nostdin"]
    )

    FFMPEG_OPTIONS = "-vn"
