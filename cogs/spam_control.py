# cogs/spam_control.py

import discord
from discord.ext import commands, tasks
from collections import defaultdict
from config import THREAD_SPAM_THRESHOLD

class SpamControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.thread_message_counts = defaultdict(int)
        self.reset_counts.start()

    def cog_unload(self):
        self.reset_counts.cancel()

    # Background task to reset message counts every minute
    @tasks.loop(minutes=1)
    async def reset_counts(self):
        self.thread_message_counts.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.Thread):
            thread_id = message.channel.id
            self.thread_message_counts[thread_id] += 1

            if self.thread_message_counts[thread_id] > THREAD_SPAM_THRESHOLD:
                await message.channel.send("This thread is being locked due to spam.")
                await message.channel.edit(locked=True)

async def setup(bot):
    await bot.add_cog(SpamControl(bot))