import discord
from discord.ext import commands, tasks
import json
import random
import os

USER_FILE = "data/users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autofarm.start()

    def cog_unload(self):
        self.autofarm.cancel()

    # --------- Helper ---------
    def ensure_user(self, user_id):
        users = load_users()
        users.setdefault(str(user_id), {"pocket": 0, "bank": 0})
        save_users(users)
        return users

    # --------- Basic Commands ---------
    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        embed = discord.Embed(title=f"{ctx.author.name}'s Balance", color=discord.Color.green())
        embed.add_field(name="Pocket", value=f"${users[user]['pocket']}", inline=True)
        embed.add_field(name="Bank", value=f"${users[user]['bank']}", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def work(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        amount = random.randint(50, 200)
        users[user]["pocket"] += amount
        save_users(users)
        embed = discord.Embed(title="Work", description=f"You worked and earned ${amount}!", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def crime(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        if random.choice([True, False]):
            amount = random.randint(100, 500)
            users[user]["pocket"] += amount
            msg = f"You succeeded in a crime and got ${amount}!"
        else:
            amount = random.randint(50, 200)
            users[user]["pocket"] -= amount
            msg = f"You failed a crime and lost ${amount}!"
        save_users(users)
        embed = discord.Embed(title="Crime", description=msg, color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def daily(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        users[user]["pocket"] += 500
        save_users(users)
        embed = discord.Embed(title="Daily Reward", description="You collected your $500 daily reward!", color=discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.command()
    async def weekly(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        users[user]["pocket"] += 2000
        save_users(users)
        embed = discord.Embed(title="Weekly Reward", description="You collected your $2000 weekly reward!", color=discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int):
        users = self.ensure_user(ctx.author.id)
        giver = str(ctx.author.id)
        receiver = str(member.id)
        users = self.ensure_user(ctx.author.id)
        users = self.ensure_user(member.id)
        if users[giver]["pocket"] < amount:
            return await ctx.send(embed=discord.Embed(title="Error", description="Not enough money!", color=discord.Color.red()))
        users[giver]["pocket"] -= amount
        users[receiver]["pocket"] += amount
        save_users(users)
        embed = discord.Embed(title="Transaction Complete", description=f"Gave ${amount} to {member.name}", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command()
    async def deposit(self, ctx, amount: int):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        if users[user]["pocket"] < amount:
            return await ctx.send(embed=discord.Embed(title="Error", description="Not enough money in pocket!", color=discord.Color.red()))
        users[user]["pocket"] -= amount
        users[user]["bank"] += amount
        save_users(users)
        await ctx.send(embed=discord.Embed(title="Deposit", description=f"Deposited ${amount} into bank.", color=discord.Color.blue()))

    @commands.command()
    async def withdraw(self, ctx, amount: int):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        if users[user]["bank"] < amount:
            return await ctx.send(embed=discord.Embed(title="Error", description="Not enough money in bank!", color=discord.Color.red()))
        users[user]["bank"] -= amount
        users[user]["pocket"] += amount
        save_users(users)
        await ctx.send(embed=discord.Embed(title="Withdraw", description=f"Withdrew ${amount} from bank.", color=discord.Color.blue()))

    # --------- Advanced Commands ---------
    @commands.command()
    async def rob(self, ctx, member: discord.Member):
        users = self.ensure_user(ctx.author.id)
        users = self.ensure_user(member.id)
        thief = str(ctx.author.id)
        victim = str(member.id)
        if users[victim]["pocket"] < 100:
            return await ctx.send(embed=discord.Embed(title="Robbery Failed", description="Target has too little money.", color=discord.Color.red()))
        if random.choice([True, False]):
            amount = random.randint(50, users[victim]["pocket"])
            users[thief]["pocket"] += amount
            users[victim]["pocket"] -= amount
            save_users(users)
            embed = discord.Embed(title="Robbery Success", description=f"You robbed ${amount} from {member.name}!", color=discord.Color.green())
        else:
            amount = random.randint(20, 100)
            users[thief]["pocket"] -= amount
            save_users(users)
            embed = discord.Embed(title="Robbery Failed", description=f"You got caught and lost ${amount}!", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def lb(self, ctx):
        users = load_users()
        sorted_users = sorted(users.items(), key=lambda x: x[1]["pocket"], reverse=True)[:10]
        desc = ""
        for i, (user_id, data) in enumerate(sorted_users, start=1):
            user = ctx.guild.get_member(int(user_id))
            desc += f"{i}. {user.name if user else 'Unknown'} - ${data['pocket']}\n"
        embed = discord.Embed(title="Top 10 Pocket Balances", description=desc, color=discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command()
    async def bankbal(self, ctx):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        await ctx.send(embed=discord.Embed(title="Bank Balance", description=f"${users[user]['bank']}", color=discord.Color.blue()))

    @commands.command()
    async def banklb(self, ctx):
        users = load_users()
        sorted_users = sorted(users.items(), key=lambda x: x[1]["bank"], reverse=True)[:10]
        desc = ""
        for i, (user_id, data) in enumerate(sorted_users, start=1):
            user = ctx.guild.get_member(int(user_id))
            desc += f"{i}. {user.name if user else 'Unknown'} - ${data['bank']}\n"
        embed = discord.Embed(title="Top 10 Bank Balances", description=desc, color=discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command()
    async def roulette(self, ctx, color: str, amount: int):
        users = self.ensure_user(ctx.author.id)
        user = str(ctx.author.id)
        if users[user]["pocket"] < amount:
            return await ctx.send(embed=discord.Embed(title="Error", description="Not enough money!", color=discord.Color.red()))
        color = color.lower()
        result = random.choice(["red", "black"])
        if color == result:
            users[user]["pocket"] += amount
            msg = f"You won ${amount}! The ball landed on {result}."
            color_embed = discord.Color.green()
        else:
            users[user]["pocket"] -= amount
            msg = f"You lost ${amount}! The ball landed on {result}."
            color_embed = discord.Color.red()
        save_users(users)
        embed = discord.Embed(title="Roulette", description=msg, color=color_embed)
        await ctx.send(embed=embed)

    # --------- Heist (Requires min 5 users) ---------
    @commands.command()
    async def heist(self, ctx):
        users = load_users()
        participating = []
        for member in ctx.guild.members:
            if str(member.id) in users and users[str(member.id)]["pocket"] >= 100:
                participating.append(member)
        if len(participating) < 5:
            return await ctx.send(embed=discord.Embed(title="Heist Failed", description="Not enough participants (min 5).", color=discord.Color.red()))
        total_loot = sum(random.randint(50, users[str(m.id)]["pocket"]) for m in participating)
        split = total_loot // len(participating)
        for m in participating:
            users[str(m.id)]["pocket"] += split
        save_users(users)
        embed = discord.Embed(title="Heist Successful", description=f"{len(participating)} people shared ${total_loot} (${split} each)!", color=discord.Color.gold())
        await ctx.send(embed=embed)

    # --------- Autofarm (Passive income) ---------
    @tasks.loop(seconds=60)
    async def autofarm(self):
        users = load_users()
        for user_id in users:
            users[user_id]["pocket"] += 10
        save_users(users)

def setup(bot):
    bot.add_cog(Economy(bot))
