from disnake import FFmpegOpusAudio


class AudioStream(FFmpegOpusAudio):
    def __init__(self, source: str):
        super().__init__(
            source,
            before_options=_PlayerOption.FFMPEG_BEFORE_OPTIONS,
            options=_PlayerOption.FFMPEG_OPTIONS,
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
    FFMPEG_BEFORE_OPTIONS = " ".join(  # noqa: FLY002
        [
            "-vn",
            "-reconnect 1",
            "-reconnect_streamed 1",
            "-reconnect_delay_max 3",
            "-nostdin",
        ]
    )

    FFMPEG_OPTIONS = ""
