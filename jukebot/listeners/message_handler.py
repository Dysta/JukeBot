from nextcord import Message
from nextcord.ext import commands


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if self._bot.user.mentioned_in(message):
            mention = f"<@!{self._bot.user.id}>"
            pure_content = message.content.replace(mention, "")
            if pure_content == "":
                ctx = await self._bot.get_context(message)
                system_cog = self._bot.get_cog("Utility")
                await ctx.invoke(system_cog.prefix)


def setup(bot):
    bot.add_cog(MessageHandler(bot))
