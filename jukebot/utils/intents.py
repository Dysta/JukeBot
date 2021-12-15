from nextcord import Intents


def get() -> Intents:
    intents = Intents.none()
    intents.guild_messages = True
    intents.guild_reactions = True
    intents.guilds = True
    intents.voice_states = True
    intents.members = True
    return intents
