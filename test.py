import requests
import json
import discord
from discord.ext import commands
from datetime import datetime

with open("token.txt") as f:
    lines = f.read()
    token = lines.split('\n', 1)[0]

bot = commands.Bot(command_prefix='$')
flag_emojis = {
    "Fast": ":rocket:",
    "Guard": ":shield:",
    "V2Dir" : ":file_folder:",
    "Valid": ":white_check_mark:",
    "Running": ":arrow_forward:",
}

def days_between(d1, d2):
    d1 = datetime.strptime(d1[:10], "%Y-%m-%d")
    return abs((d2 - d1).days)

@bot.command()
async def tor_relay(ctx, nickname):
    r = requests.get('https://onionoo.torproject.org/details')
    response = r.json()
    for i in response['relays']:
        if i['nickname'] == nickname:
            embed = discord.Embed(title=i['nickname'])
            embed.add_field(name='Uptime', value=f"{days_between(i['last_restarted'], datetime.now())} days", inline=False)
            embed.add_field(name='Country', value=f":flag_{i['country']}:", inline=False)
            embed.add_field(name='Flags', value=i['flags'], inline=False)
            await ctx.send(embed=embed)
bot.run(token)