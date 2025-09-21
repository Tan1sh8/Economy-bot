import discord
from discord.ext import commands
import json

USER_FILE = "data/users.json"

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetuser(self, ctx, member: discord.Member):
        users = load_users()
        users[str(member.id)] = {"pocket": 0, "bank": 0}
        save_users(users)
        await ctx.send(embed=discord.Embed(title="Reset User", description=f"{member.name}'s balance has been reset.", color=discord.Color.red()))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, member: discord.Member, amount: int):
        users = load_users()
        users.setdefault(str(member.id), {"pocket": 0, "bank": 0})
        users[str(member.id)]["pocket"] += amount
        save_users(users)
        await ctx.send(embed=discord.Embed(title="Money Added", description=f"${amount} added to {member.name}'s pocket.", color=discord.Color.green()))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx, member: discord.Member, amount: int):
        users = load_users()
        users.setdefault(str(member.id), {"pocket": 0, "bank": 0})
        users[str(member.id)]["pocket"] -= amount
        save_users(users)
        await ctx.send(embed=discord.Embed(title="Money Removed", description=f"${amount} removed from {member.name}'s pocket.", color=discord.Color.red()))

def setup(bot):
    bot.add_cog(Admin(bot))
