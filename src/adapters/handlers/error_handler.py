import discord
import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        log.info("ErrorHandlerCog loaded.")

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError
    ):
        log.error(f"Command '{ctx.command.qualified_name}' failed.", exc_info=error)
        
        embed = discord.Embed(
            title="Command Error",
            description="An unexpected error occurred while running this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Please contact the administrator if this issue persists.")
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot, use_cases: dict):
    await bot.add_cog(ErrorHandlerCog(bot))