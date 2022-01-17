import os
import nextcord

from nextcord import Member, Interaction

from jukebot.components import ResultSet


class SearchInteraction:
    CANCEL_REACTION = "❌"
    CANCEL_TEXT = "Cancel"
    NUMBER_REACTION = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "🔟",
    ]


class _SearchDropdown(nextcord.ui.Select):
    def __init__(self, results: ResultSet):
        self._results = results
        options = [
            nextcord.SelectOption(
                label=r.title,
                value=r.web_url,
                description=f"on {r.channel} — {r.fmt_duration}",
                emoji=SearchInteraction.NUMBER_REACTION[i],
            )
            for i, r in enumerate(results)
        ]
        options.append(
            nextcord.SelectOption(
                label="Cancel",
                value=SearchInteraction.CANCEL_TEXT,
                description="Cancel the current search",
                emoji=SearchInteraction.CANCEL_REACTION,
            )
        )

        super().__init__(
            placeholder="Choose a song...",
            min_values=1,
            max_values=1,
            options=options,
        )


class SearchDropdownView(nextcord.ui.View):
    def __init__(self, author: Member, results: ResultSet):
        super().__init__(timeout=float(os.environ["BOT_SEARCH_TIMEOUT"]))
        self._author = author
        self._drop = _SearchDropdown(results)
        self.add_item(self._drop)
        self._timeout = False

    async def interaction_check(self, interaction: Interaction):
        if self._author != interaction.user:
            return
        self.stop()

    async def on_timeout(self) -> None:
        self._timeout = True

    @property
    def result(self):
        return (
            self._drop.values[0] if not self._timeout else SearchInteraction.CANCEL_TEXT
        )
