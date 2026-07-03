import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from src.database import Database
from src.cogs.timesheet import TimesheetCog
from src.cogs.vehicles import VehiclesCog
from src.cogs.incidents import IncidentsCog

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('DISCORD_PREFIX', '!'), intents=intents)

# Database
db = Database()

@bot.event
async def on_ready():
    """Bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    await db.initialize()
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argumento faltando: {error.param}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ Erro: {str(error)}")

async def load_cogs():
    """Load all cogs"""
    logger.info("Loading cogs...")
    
    cogs = [
        TimesheetCog,
        VehiclesCog,
        IncidentsCog
    ]
    
    for cog in cogs:
        try:
            await bot.add_cog(cog(bot, db))
            logger.info(f"✓ Loaded {cog.__name__}")
        except Exception as e:
            logger.error(f"Failed to load {cog.__name__}: {e}")

async def main():
    """Start the bot"""
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
