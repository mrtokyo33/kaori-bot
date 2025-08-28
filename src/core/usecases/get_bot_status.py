import discord
from discord.ext import commands
from src.core.entities.bot_status import BotStatus

class GetBotStatusUseCase:
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    def execute(self) -> BotStatus:
        return BotStatus(
            is_online=not self._bot.is_closed(),
            latency=self._bot.latency,
            guild_count=len(self._bot.guilds)
        )