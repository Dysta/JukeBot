import nextcord


class _JoinActivityButton(nextcord.ui.Button):
    def __init__(self, url):
        label = "Join the activity"
        emoji = "🌠"

        super().__init__(url=url, label=label, emoji=emoji)


class ActivityView(nextcord.ui.View):
    def __init__(self, code):
        super(ActivityView, self).__init__()
        self.add_item(_JoinActivityButton(code))
