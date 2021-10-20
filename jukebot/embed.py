import discord


class Embed:
    @staticmethod
    def error_message(title="", content="", footer=""):
        embed = discord.Embed(title=title, description=content, color=0xFF0000)
        embed.set_author(
            name="Error",
            icon_url="https://icons.iconarchive.com/icons/papirus-team/papirus-status/32/dialog-error-icon.png",
        )
        if not footer == "":
            embed.set_footer(text=footer)

        return embed
