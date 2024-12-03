import discord
from discord.ext import commands
from collections import defaultdict
import time

class SpamControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_threads = defaultdict(list)  # Tracks thread creation times per user
        self.user_posts = defaultdict(list)   # Tracks thread posts per user in channels
        self.thread_limit = 3                 # Max threads per user within time window
        self.time_window = 600                # Time window in seconds (10 minutes)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        user = thread.owner
        now = time.time()

        # Track thread creation times
        self.user_threads[user.id] = [
            t for t in self.user_threads[user.id] if now - t < self.time_window
        ]
        self.user_threads[user.id].append(now)

        # Check if thread creation exceeds limit
        if len(self.user_threads[user.id]) > self.thread_limit:
            await thread.delete()
            await user.send(
                f"⚠️ You have exceeded the thread creation limit in {thread.guild.name}. Please wait before creating more threads."
            )
            print(f"Deleted spam thread by {user.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type != discord.ChannelType.public_thread:
            return  # Ignore non-thread messages

        user = message.author
        channel = message.channel

        # Track user posts in threads
        now = time.time()
        self.user_posts[user.id].append((channel.id, now))

        # Check for duplicate posts across channels
        recent_posts = [
            post for post in self.user_posts[user.id] if now - post[1] < self.time_window
        ]
        channels_posted = {post[0] for post in recent_posts}

        if len(channels_posted) > 1:  # User is spamming across multiple threads
            await message.delete()
            await user.send(
                f"⚠️ Please avoid spamming your content across multiple threads in {message.guild.name}."
            )
            print(f"Deleted spam message by {user.name} in {channel.name}")

async def setup(bot):
    await bot.add_cog(SpamControlCog(bot))
