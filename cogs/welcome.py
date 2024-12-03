# cogs/welcome.py

import discord
from discord.ext import commands
from config import WELCOME_CHANNEL

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event listener for when a member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
        if channel:
            embed = discord.Embed(
                title="Welcome to the Server!",
                description=f"Hello {member.mention}, welcome to our community!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Getting Started", value="Please read the rules and introduce yourself.", inline=False)
            await channel.send(embed=embed)

    # Command for onboarding
    @commands.command()
    async def start(self, ctx):
        embed = discord.Embed(
            title="Welcome!",
            description="Let's get you started.",
            color=discord.Color.green()
        )
        embed.add_field(name="Step 1", value="Read the rules.", inline=False)
        embed.add_field(name="Step 2", value="Introduce yourself.", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))