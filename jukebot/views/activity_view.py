import disnake


class _JoinActivityButton(disnake.ui.Button):
    def __init__(self, url):
        label = "Join the activity"
        emoji = "🌠"

        super().__init__(url=url, label=label, emoji=emoji)


class ActivityView(disnake.ui.View):
    def __init__(self, code):
        super().__init__()
        self.add_item(_JoinActivityButton(code))
