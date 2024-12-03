# cogs/thread_management.py

import discord
from discord.ext import commands, tasks
import datetime

class ThreadManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_archived_threads.start()

    def cog_unload(self):
        self.check_archived_threads.cancel()

    # Command to create a thread
    @commands.command()
    async def createthread(self, ctx, *, thread_name):
        thread = await ctx.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        await thread.send(f"{ctx.author.mention} has created this thread.")

    # Background task to auto-archive inactive threads
    @tasks.loop(hours=1)
    async def check_archived_threads(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                threads = channel.threads
                for thread in threads:
                    if thread.locked or thread.archived:
                        continue
                    # Auto-archive threads inactive for 24 hours
                    last_message = thread.last_message
                    if last_message:
                        time_diff = discord.utils.utcnow() - last_message.created_at
                        if time_diff.total_seconds() > 86400:
                            await thread.edit(archived=True)

async def setup(bot):
    await bot.add_cog(ThreadManagement(bot))