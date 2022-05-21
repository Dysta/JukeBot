from disnake import Intents


def get() -> Intents:
    intents = Intents.none()
    intents.guild_messages = True
    intents.guilds = True
    intents.voice_states = True
    intents.members = True
    intents.message_content = True
    return intents
