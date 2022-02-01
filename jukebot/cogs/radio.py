import random

from loguru import logger

from nextcord.ext import commands
from nextcord.ext.commands import Bot, Context, BucketType

from jukebot.checks import voice


class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def _radio_process(self, ctx: Context, choices: list):
        n: int = random.randint(0, len(choices) - 1)
        query: str = choices[n]
        logger.opt(lazy=True).debug(f"Choice number {n} is {query}")
        music_cog = self.bot.get_cog("Music")
        await ctx.invoke(music_cog.play, query=query)

    @commands.command(
        brief="Launch a random lofi radio", help="Launch a random lofi radio"
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def lofi(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=5qap5aO4i9A",
            "https://www.youtube.com/watch?v=DWcJFNfaw9c",
            "https://www.youtube.com/watch?v=kgx4WGK0oNU",
            "https://www.youtube.com/watch?v=xgirCNccI68",
            "https://www.youtube.com/watch?v=7NOSDKb0HlU",
            "https://www.youtube.com/watch?v=j28Oyq6NnOs",
            "https://www.youtube.com/watch?v=l7TxwBhtTUY",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        brief="Launch a random jazz radio", help="Launch a random jazz radio"
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def jazz(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=Dx5qFachd3A",
            "https://www.youtube.com/watch?v=fEvM-OUbaKs",
            "https://www.youtube.com/watch?v=g06AjrOlki0",
            "https://www.youtube.com/watch?v=DSGyEsJ17cI",
            "https://www.youtube.com/watch?v=NgS8eiq-4rs",
            "https://www.youtube.com/watch?v=XnzxEGLaPxs",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["rnr", "r&r"],
        brief="Launch a random rock n roll radio",
        help="Launch a random rock n roll radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def rocknroll(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=cVCfu_KPiR8",
            "https://www.youtube.com/watch?v=qMnyF6tampA",
            "https://www.youtube.com/watch?v=5X18D-EbjUc",
            "https://www.youtube.com/watch?v=pT9RPH-ga9w",
            "https://www.youtube.com/playlist?list=PLZN_exA7d4RVmCQrG5VlWIjMOkMFZVVOc",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["ct", "8bits"],
        brief="Launch a random chiptune radio",
        help="Launch a random chiptune radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def chiptune(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=otobhj8X1_Q",
            "https://www.youtube.com/watch?v=KzFmtxFG9z4",
            "https://www.youtube.com/watch?v=QLM7HwdRwsk",
            "https://www.youtube.com/watch?v=Hzaw1ZLMCNs",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["sw", "vw", "vaporwave"],
        brief="Launch a random synthwave radio",
        help="Launch a random synthwave radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def synthwave(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=q5OjZhOYhow",
            "https://www.youtube.com/watch?v=xxgxkjV70Vc",
            "https://www.youtube.com/watch?v=csJT1QKSulA",
            "https://www.youtube.com/watch?v=hNmWvk_mUVE",
            "https://www.youtube.com/playlist?list=PL9a7fFpVuuJCNx1VfUKlusNP-4TGBTuz5",
            "https://www.youtube.com/watch?v=628wiazhrKA",
            "https://www.youtube.com/watch?v=xLk9ZaguQVc",
            "https://www.youtube.com/watch?v=5vgw9F5CZRQ",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["coffee", "loungecoffee"],
        brief="Launch a random lounge coffee radio",
        help="Launch a random lounge coffee radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def lounge(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=fEvM-OUbaKs",
            "https://www.youtube.com/watch?v=Dx5qFachd3A",
            "https://www.youtube.com/watch?v=XQuR1OxYJt0",
            "https://www.youtube.com/watch?v=3XbEUv_MCj0",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["mc"],
        brief="Launch a random Minecraft OST radio",
        help="Launch a random Minecraft OST radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def minecraft(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=Pa_s7ogtokM",
            "https://www.youtube.com/watch?v=TsTtqGAxvWk",
            "https://www.youtube.com/watch?v=Dg0IjOzopYU",
            "https://www.youtube.com/watch?v=snphzO9UFJM",
            "https://www.youtube.com/watch?v=0KvlwMd3C4Y",
            "https://www.youtube.com/playlist?list=PL3817D41C7D841E23",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        brief="Launch a random rap radio", help="Launch a random rap radio"
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def rap(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=05689ErDUdM",
            "https://www.youtube.com/watch?v=n4pr7j-kTO0",
            "https://www.youtube.com/watch?v=kmwxyLnGegw",
            "https://www.youtube.com/watch?v=dATRhAwzM9E",
            "https://www.youtube.com/watch?v=pKKIxeMIv78",
            "https://www.youtube.com/watch?v=n7rPvz7Rr1Q",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["indie", "popr"],
        brief="Launch a random poprock/indie radio",
        help="Launch a random poprock/indie radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def poprock(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=1itSqkbXIlU",
            "https://www.youtube.com/watch?v=oVi5gtzTDx0",
            "https://www.youtube.com/watch?v=5X18D-EbjUc",
            "https://www.youtube.com/watch?v=3Hqn5MEL5Kc",
            "https://www.youtube.com/watch?v=DjkOpbchPcM",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["gym"],
        brief="Launch a random gym/workout radio",
        help="Launch a random gym/workout radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def workout(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/watch?v=iIPKxEghUzA",
            "https://www.youtube.com/watch?v=Jao_r4NcloY",
            "https://www.youtube.com/watch?v=As96HhiUwXo",
            "https://www.youtube.com/watch?v=1E8q1cvNjOA",
            "https://www.youtube.com/watch?v=qWf-FPFmVw0",
        ]
        await self._radio_process(ctx, choices)

    @commands.command(
        aliases=["reverb", "slowreverb"],
        brief="Launch a random slowed+reverb radio",
        help="Launch a random slowed+reverb radio",
    )
    @commands.cooldown(1, 5.0, BucketType.user)
    @commands.guild_only()
    @commands.check(voice.user_is_connected)
    async def slowed(self, ctx: Context):
        choices: list = [
            "https://www.youtube.com/playlist?list=PLF_ZnpSKNQQFTeHaQ1ZR5l5cx5nRiD80w",
            "https://www.youtube.com/playlist?list=PLsmLp2JHrigK1FBB-nuy3panZJzH5sHWO",
            "https://www.youtube.com/watch?v=JAw4tcjzd1c",
        ]
        await self._radio_process(ctx, choices)


def setup(bot):
    bot.add_cog(Radio(bot))
