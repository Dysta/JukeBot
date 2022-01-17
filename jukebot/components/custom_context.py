import os
import random

from nextcord.ext.commands import Context

from jukebot.views import PromoteView


class CustomContext(Context):
    async def invoke(self, command, /, *args, **kwargs):
        self.bot.dispatch("command_invoked", self, command)
        return await super().invoke(command, *args, **kwargs)

    async def reply(self, content=None, **kwargs):
        if not "view" in kwargs and os.environ["USE_PROMOTE_VIEW"] == "true":
            if random.randint(0, 100) <= int(
                os.environ["PERCENT_PROMOTE_VIEW_APPEARANCE"]
            ):
                kwargs["view"] = PromoteView()

        return await super().reply(content=content, **kwargs)

    async def send(
        self,
        content=None,
        *,
        tts=None,
        embed=None,
        embeds=None,
        file=None,
        files=None,
        stickers=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        reference=None,
        mention_author=None,
        view=None,
    ):
        if not view and os.environ["USE_PROMOTE_VIEW"] == "true":
            if random.randint(0, 100) <= int(
                os.environ["PERCENT_PROMOTE_VIEW_APPEARANCE"]
            ):
                view = PromoteView()

        return await super().send(
            content=content,
            tts=tts,
            embed=embed,
            file=file,
            stickers=stickers,
            delete_after=delete_after,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
            reference=reference,
            mention_author=mention_author,
            view=view,
        )
