from nextcord import FFmpegPCMAudio, AudioSource


class AudioStream(AudioSource):
    def __init__(self, source: FFmpegPCMAudio):
        self._source: FFmpegPCMAudio = source
        self._progress: int = 0

    def read(self) -> bytes:
        data = self._source.read()
        if data:
            self._progress += 1
        return data

    def cleanup(self) -> None:
        self._source.cleanup()

    @property
    def progress(self) -> int:
        # 20ms
        return int(self._progress * 0.02)
