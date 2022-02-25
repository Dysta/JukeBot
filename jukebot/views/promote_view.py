import nextcord
import os


class _VoteButton(nextcord.ui.Button):
    def __init__(self):
        url = os.environ["BOT_VOTE_URL"]
        label = "Vote"
        emoji = "📈"

        super().__init__(url=url, label=label, emoji=emoji)


class _InviteButton(nextcord.ui.Button):
    def __init__(self):
        url = os.environ["BOT_INVITE_URL"]
        label = "Invite me"
        emoji = "➕"

        super().__init__(url=url, label=label, emoji=emoji)


class _DonateButton(nextcord.ui.Button):
    def __init__(self):
        url = os.environ["BOT_DONATE_URL"]
        label = "Donate"
        emoji = "✨"

        super().__init__(url=url, label=label, emoji=emoji)


class _ServerButton(nextcord.ui.Button):
    def __init__(self):
        url = os.environ["BOT_SERVER_URL"]
        label = "Community"
        emoji = "🫂"

        super().__init__(url=url, label=label, emoji=emoji)


class PromoteView(nextcord.ui.View):
    def __init__(self):
        super(PromoteView, self).__init__()
        self.add_item(_InviteButton())
        self.add_item(_VoteButton())
        self.add_item(_ServerButton())
        self.add_item(_DonateButton())
