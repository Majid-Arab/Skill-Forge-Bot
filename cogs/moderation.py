# cogs/moderation.py

import discord
from discord.ext import commands
from config import PROHIBITED_WORDS, SCAM_LINKS

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event listener for message events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Language Moderation
        if any(word in message.content.lower() for word in PROHIBITED_WORDS):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please watch your language!")
            return

        # Scam and Spam Detection
        if any(link in message.content for link in SCAM_LINKS):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, scam links are not allowed!")
            return

async def setup(bot):
    await bot.add_cog(Moderation(bot))