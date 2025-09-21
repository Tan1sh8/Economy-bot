
---

README.md

# Discord Economy Bot

A fully featured Discord economy bot with pocket & bank system, work, crime, daily/weekly rewards, rob, heist, roulette, leaderboards, and admin commands. All commands respond using **embeds**.

---

## 📦 Setup

1. **Clone the repository then:**

cd discord-economy-bot

2. **Install requirements:**

pip install discord.py

3. **Configure your bot:**
- Open `config.json` and add your bot token:
```json
{
  "prefix": ".",
  "token": "YOUR_BOT_TOKEN"
}
```
4. Run the bot:



python main.py


---

💰 Economy Commands

Command	Description

.balance / .bal	Shows your pocket and bank balance
.work	Earn a random amount of money
.crime	Attempt a risky crime, gain or lose money
.daily	Collect daily $500 reward
.weekly	Collect weekly $2000 reward
.give @user amount	Give money to another user
.deposit amount	Deposit money from pocket to bank
.withdraw amount	Withdraw money from bank to pocket
.rob @user	Attempt to rob another user
.lb	Top 10 pocket balances
.bankbal	Check your bank balance
.banklb	Top 10 bank balances
.roulette color amount	Bet on red or black in roulette
.heist	Participates in a heist (min 5 users)
.autofarm	Passive income added every minute


> Note: Autofarm runs automatically every 60 seconds (+$10 per user)




---

🛡 Admin Commands

Command	Description

.resetuser @user	Reset a user’s pocket & bank balance
.addmoney @user amount	Add money to a user’s pocket
.removemoney @user amount	Remove money from a user’s pocket


> Requires administrator permissions




---

⚙️ Adding More Commands

1. Open cogs/economy.py (for economy commands) or cogs/admin.py (for admin commands)


2. Add a new command using the standard Discord.py Cog structure:



@commands.command()
async def newcommand(self, ctx):
    embed = discord.Embed(
        title="Title",
        description="Your description here",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

3. Save the file and restart the bot to load the new command.




---

🗂 File Structure

discord-economy-bot/
│
├─ cogs/
│   ├─ economy.py       # Economy commands
│   └─ admin.py         # Admin commands
│
├─ data/
│   └─ users.json       # JSON database for users
├─ config.json          # Bot settings (prefix & token)
├─ main.py              # Bot entry point
└─ README.md            # This file


---

⚠ Notes

Ensure your bot has Send Messages and Embed Links permissions in your Discord server.

All monetary data is stored in data/users.json. Make backups to avoid loss.

Heist requires at least 5 participants with at least $100 in pocket to succeed.



---

🎉 Contributions

Feel free to fork this repo, add new features, or improve the economy system. Always restart the bot after adding new commands.
