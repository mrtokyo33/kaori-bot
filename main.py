import discord
from discord.ext import commands
import os
import logging
from importlib import import_module

from src.infrastructure.config.settings import settings
from src.infrastructure.logging.logger import setup_logging

from src.core.usecases.get_bot_status import GetBotStatusUseCase
from src.core.usecases.say_hello import SayHelloUseCase

setup_logging()
log = logging.getLogger(__name__)

def setup_intents() -> discord.Intents:
    intents_config = settings.bot_config.get('intents', {})
    intents = discord.Intents.default()
    

    for intent_name, is_enabled in intents_config.items():
        if hasattr(intents, intent_name):
            setattr(intents, intent_name, is_enabled)
            log.info(f"Intent '{intent_name}' set to {is_enabled}")
            
    return intents

async def main():
    bot = commands.Bot(command_prefix="!", intents=setup_intents())

    use_cases = {
        "get_bot_status": GetBotStatusUseCase(bot=bot),
        "say_hello": SayHelloUseCase(
            hello_message=settings.messages_config.get('hello', 'Hello!')
        ),
    }

    extensions_path = settings.bot_config.get('extensions_path', 'src.adapters.cogs')
    base_path = extensions_path.replace('.', '/') 
    
    handler_path_str = "src.adapters.handlers"
    handler_path_fs = handler_path_str.replace('.', '/')

    for path, path_str in [(base_path, extensions_path), (handler_path_fs, handler_path_str)]:
        for filename in os.listdir(path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    module = import_module(f'{path_str}.{module_name}')
                    if hasattr(module, 'setup'):
                        await module.setup(bot, use_cases)
                    else:
                        log.warning(f"Adapter '{module_name}' has no setup function.")
                except Exception as e:
                    log.error(f"Failed to load adapter '{module_name}'.", exc_info=e)

    @bot.event
    async def on_ready():
        log.info(f'Bot logged in as {bot.user} (ID: {bot.user.id})')
        
        # Sync slash commands
        try:
            synced = await bot.tree.sync()
            log.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            log.error(f"Failed to sync commands: {e}")
        
        bot_cfg = settings.bot_config
        status_map = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible,
        }
        activity_map = {
            "playing": discord.ActivityType.playing,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
        }
        
        status = status_map.get(bot_cfg.get('status', 'online'))
        activity_type = activity_map.get(bot_cfg.get('activity_type', 'playing'))
        activity_name = bot_cfg.get('activity_name', 'Kaori Bot')
        
        activity = discord.Activity(type=activity_type, name=activity_name)
        await bot.change_presence(status=status, activity=activity)
        
        log.info('------ Kaori-bot is ready! ------')

    await bot.start(settings.discord_bot_token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())