class Extensions:
    exts = (
        {"package": "jukebot.listeners", "name": "logger_handler"},
        {"package": "jukebot.listeners", "name": "error_handler"},
        {"package": "jukebot.listeners", "name": "voice_handler"},
        {"package": "jukebot.cogs", "name": "utility"},
        {"package": "jukebot.cogs", "name": "music"},
        {"package": "jukebot.cogs", "name": "system"},
        {"package": "jukebot.cogs", "name": "search"},
        {"package": "jukebot.cogs", "name": "queue"},
        {"package": "jukebot.cogs", "name": "radio"},
    )

    @staticmethod
    def all():
        return Extensions.exts

    @staticmethod
    def get(name):
        for e in Extensions.exts:
            if e["name"] == name:
                return e
        return None

    def __repr__(self):
        return self.exts.__repr__()
