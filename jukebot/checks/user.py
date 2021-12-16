from nextcord.ext.commands import Context, CheckFailure


def is_dysta(ctx: Context):
    if not ctx.message.author.id == 845189167914549288:
        raise CheckFailure("You're not Dysta.")
    return True
