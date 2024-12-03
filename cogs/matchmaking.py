# cogs/matchmaking.py

import discord
from discord.ext import commands

class Matchmaking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.buyers = []
        self.sellers = []

    @commands.command()
    async def buy(self, ctx, *, item):
        self.buyers.append({'user': ctx.author, 'item': item})
        await ctx.send(f"{ctx.author.mention} is looking to buy: {item}")
        await self.match_users(ctx)

    @commands.command()
    async def sell(self, ctx, *, item):
        self.sellers.append({'user': ctx.author, 'item': item})
        await ctx.send(f"{ctx.author.mention} is selling: {item}")
        await self.match_users(ctx)

    async def match_users(self, ctx):
        for buyer in self.buyers:
            for seller in self.sellers:
                if buyer['item'].lower() == seller['item'].lower():
                    await ctx.send(f"Match found! {buyer['user'].mention} and {seller['user'].mention} are both interested in {buyer['item']}.")
                    self.buyers.remove(buyer)
                    self.sellers.remove(seller)
                    return

async def setup(bot):
    await bot.add_cog(Matchmaking(bot))