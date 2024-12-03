import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.name} has joined the server.")  # Log the join event
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if channel:
            print(f"Found the channel: {channel.name}")  # Log channel detection
            embed = discord.Embed(
                title="Welcome to the Server!",
                description=f"Hi {member.mention}, welcome!",
                color=discord.Color.blue()
            )
            await channel.send(embed=embed)
        else:
            print("Welcome channel not found.")


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
    
    
