class Extensions:
    __list__ = [
        {"package": "jukebot.listeners", "name": "logger_handler"},
        {"package": "jukebot.listeners", "name": "error_handler"},
        {"package": "jukebot.listeners", "name": "voice_handler"},
        {"package": "jukebot.listeners", "name": "message_handler"},
        {"package": "jukebot.cogs", "name": "utility"},
        {"package": "jukebot.cogs", "name": "music"},
        {"package": "jukebot.cogs", "name": "system"},
        {"package": "jukebot.cogs", "name": "search"},
        {"package": "jukebot.cogs", "name": "queue"},
    ]

    @staticmethod
    def all():
        return Extensions.__list__

    @staticmethod
    def get(name):
        for e in Extensions.__list__:
            if e["name"] == name:
                return e
        else:
            return None

    def __repr__(self):
        return self.__list__.__repr__()
