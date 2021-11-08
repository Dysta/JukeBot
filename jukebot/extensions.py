class Extensions:
    __list__ = [
        {"package": "listeners", "name": "error_handler"},
        {"package": "cogs", "name": "utility"},
        {"package": "cogs", "name": "music"},
        {"package": "cogs", "name": "system"},
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
