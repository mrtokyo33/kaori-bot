import discord
import logging
from discord.ext import commands
from discord import app_commands

from src.core.usecases.say_hello import SayHelloUseCase
log = logging.getLogger(__name__)

class HelloCog(commands.Cog):
    def __init__(self, say_hello_use_case: SayHelloUseCase):
        self.say_hello_use_case = say_hello_use_case
        log.info("HelloCog loaded.")

    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: discord.Interaction):
        message = self.say_hello_use_case.execute()
        
        await interaction.response.send_message(f"{message}")

async def setup(bot: commands.Bot, use_cases: dict):
    await bot.add_cog(HelloCog(use_cases['say_hello']))