import discord
import logging
from discord.ext import commands
from discord import app_commands

from src.core.usecases.get_bot_status import GetBotStatusUseCase

log = logging.getLogger(__name__)

class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot, get_bot_status_use_case: GetBotStatusUseCase):
        self.bot = bot
        self.get_bot_status_use_case = get_bot_status_use_case
        log.info("StatusCog loaded.")

    @app_commands.command(name="status", description="Shows the status and latency of Kaori-bot.")
    async def status(self, interaction: discord.Interaction):
        """Controller: Receives the command, calls the usecase, and presents the result."""
        await interaction.response.defer()
        
        status_data = self.get_bot_status_use_case.execute()

        embed = discord.Embed(
            title="Kaori-bot Status",
            color=discord.Color.green() if status_data.is_online else discord.Color.red()
        )
        embed.add_field(name="Status", value="Online" if status_data.is_online else "Offline", inline=True)
        embed.add_field(name="Latency", value=f"{status_data.latency * 1000:.2f} ms", inline=True)
        embed.add_field(name="Servers", value=str(status_data.guild_count), inline=True)
        embed.set_footer(text=f"Powered by {self.bot.user.name}")

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot, use_cases: dict):
    await bot.add_cog(StatusCog(bot, use_cases['get_bot_status']))