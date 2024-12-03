# cogs/recap.py

import discord
from discord.ext import commands, tasks
from config import GENERAL_CHANNEL
import datetime

class Recap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_recap.start()

    def cog_unload(self):
        self.daily_recap.cancel()

    # Background task to send daily recap
    @tasks.loop(hours=24)
    async def daily_recap(self):
        await self.bot.wait_until_ready()
        channel = discord.utils.get(self.bot.get_all_channels(), name=GENERAL_CHANNEL)
        if channel:
            embed = discord.Embed(
                title="Daily Recap",
                description="Here's what happened today!",
                color=discord.Color.blue()
            )
            # Add your recap logic here
            await channel.send(embed=embed)

    @daily_recap.before_loop
    async def before_daily_recap(self):
        now = datetime.datetime.utcnow()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        await discord.utils.sleep_until(next_run)

async def setup(bot):
    await bot.add_cog(Recap(bot))