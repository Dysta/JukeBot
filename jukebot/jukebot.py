import nextcord
from datetime import datetime
from nextcord.ext import commands


class JukeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._activity = nextcord.Game("Juke goes brrr")
        self._start = None

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        self._start = datetime.now()
        await self.change_presence(
            status=nextcord.Status.online, activity=self._activity
        )

    async def on_error(self, event, *args, **kwargs):
        print(f"{event=}{args}{kwargs}")

    @property
    def start_time(self):
        return self._start
