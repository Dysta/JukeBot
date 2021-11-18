import discord
from concurrent.futures import ProcessPoolExecutor


class AudioStream(discord.AudioSource):
    def __init__(self, source):
        self._source = source
        self._progress = 0

    def read(self) -> bytes:
        data = self._source.read()
        if data:
            self._progress += 1
        return data

    def cleanup(self) -> None:
        self._source.cleanup()

    @property
    def progress(self) -> float:
        # 20ms
        return self._progress * 0.02
