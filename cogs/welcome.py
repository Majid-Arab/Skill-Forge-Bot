import discord
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} joined the server.")  # Logs the member join event

        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if not channel:
            print("Welcome channel not found.")
            return

        print(f"Sending welcome message to {member}.")
        embed = discord.Embed(
            title="Welcome!",
            description=f"Hi {member.mention}, glad to have you here!",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
    
    
