from disnake import Intents


def get() -> Intents:
    intents = Intents.none()
    intents.guilds = True
    intents.voice_states = True
    return intents
