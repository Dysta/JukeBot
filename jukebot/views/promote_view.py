import nextcord


class _VoteButton(nextcord.ui.Button):
    def __init__(self):
        url = "https://top.gg/bot/899039383011885176/vote"
        label = "Vote!"
        emoji = "📈"

        super().__init__(url=url, label=label, emoji=emoji)


class _InviteButton(nextcord.ui.Button):
    def __init__(self):
        url = "https://dsc.gg/jukebot"
        label = "Invite me!"
        emoji = "📥"

        super().__init__(url=url, label=label, emoji=emoji)


class PromoteView(nextcord.ui.View):
    def __init__(self):
        super(PromoteView, self).__init__()
        self.add_item(_InviteButton())
        self.add_item(_VoteButton())
