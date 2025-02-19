import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.members = True  # This enables on_member_join event
bot = commands.Bot(command_prefix="!", intents=intents)
intents.guilds = True
intents.members = True
intents.message_content = True

# Load cogs dynamically
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Bot is connected to the following servers: {[guild.name for guild in bot.guilds]}")

# Automatically load all cogs from the cogs folder
try:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cog: {filename}")
except Exception as e:
    print(f"Failed to load cog {filename}: {e}")


# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv("BOT_TOKEN"))
