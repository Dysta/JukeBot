import discord


class Embed:
    VOID_TOKEN = "\u200B"

    @staticmethod
    def error_message(ctx, title="", content=""):
        embed = discord.Embed(title="", description=content, color=0xDB3C30)
        embed.set_author(
            name="Error" if title == "" else title,
            icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-error-icon.png",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )

        return embed

    @staticmethod
    def info_message(ctx, title="", content=""):
        embed = discord.Embed(title="", description=content, color=0x30A3DB)
        embed.set_author(
            name="Information" if title == "" else title,
            icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/512/dialog-information-icon.png",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )

        return embed

    @staticmethod
    def basic_message(ctx, title="", content=""):
        embed = discord.Embed(title="", description=content, color=0x4F4F4F)
        embed.set_author(
            name="Information" if title == "" else title,
            icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/katomic-icon.png",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )

        return embed

    @staticmethod
    def music_message(ctx, title="", content="", url=""):
        embed = discord.Embed(title="", description=content, color=0x23C197)
        embed.set_author(
            name="Music" if title == "" else title,
            url=url,
            icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/enjoy-music-player-icon.png",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )

        return embed
