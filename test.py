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
    if abs((d2 - d1).days) > 1 or abs((d2 - d1).days) == 0:
        return f"{abs((d2 - d1).days)} days"
    else:
        return f"{abs((d2 - d1).days)} day"

@bot.command()
async def tor_relay(ctx, nickname):
    r = requests.get('https://onionoo.torproject.org/details')
    response = r.json()
    for i in response['relays']:
        if i['nickname'].casefold() == nickname.casefold() or i['fingerprint'] == nickname.upper():
            if i['running'] == False:
                status = ":red_circle:"
                color = 0xe74c3c
            elif 'overload_general_timestamp' in i:
                status = ":yellow_circle:"
                color = 0xf1c40f
            else:
                status = ":green_circle:"
                color = 0x2ecc71
            embed = discord.Embed(title=f"{status} {i['nickname']}", color=color)
            embed.add_field(name='Uptime', value=f"{days_between(i['last_restarted'], datetime.now())}", inline=False)
            embed.add_field(name='Country', value=f":flag_{i['country']}: {i['country_name']}", inline=False)
            embed.add_field(name='Flags', value=i['flags'], inline=False)
            embed.add_field(name='Version', value=i['version'], inline=False)
            embed.add_field(name='Fingerprint', value=i['fingerprint'], inline=False)
            if 'contact' in i:
                embed.add_field(name='Contact Info', value=i['contact'], inline=False)
            else:
                embed.add_field(name='Contact Info', value="none", inline=False)
            await ctx.send(embed=embed)
bot.run(token)