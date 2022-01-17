from nextcord.ext.commands import Context


class CustomContext(Context):
    async def invoke(self, command, /, *args, **kwargs):
        self.bot.dispatch("command_invoked", self, command)
        return await super().invoke(command, *args, **kwargs)
