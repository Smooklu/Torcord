import requests
import json
import discord
from discord.ext import commands
from datetime import datetime
import re

with open("token.txt") as f:
    lines = f.read()
    token = lines.split("\n", 1)[0]

bot = commands.Bot(command_prefix="$")
flag_emojis = {
    "Authority": ":police_officer:",
    "BadExit": ":no_entry:",
    "Exit": ":arrow_down:",
    "Fast": ":zap:",
    "Guard": ":shield:",
    "HSDir": ":green_book:",
    "Running": ":bulb:",
    "Stable": ":scales:",
    "V2Dir": ":blue_book:",
    "Valid": ":white_check_mark:",
}


def unit_plural(value, unit):
    ret = f"{value} {unit}"
    if value != 1:
        ret += "s"
    return ret


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    td = abs(d2 - d1)
    if td.days == 0:
        return (
            unit_plural(td.seconds // 3600, "hour")
            + " "
            + unit_plural(td.seconds % 60, "minute")
        )
    ret = ""
    if td.days >= 365:
        ret += unit_plural(td.days // 365, "year") + " "
    ret += unit_plural(td.days % 365, "day")
    return ret


def change_flags(list):
    for i, e in enumerate(list):
        temp = flag_emojis.get(e)
        if temp != None:
            list[i] = temp + e
    return list


@bot.command()
async def tor_relay(ctx, nickname):
    await ctx.channel.trigger_typing()
    r = requests.get("https://onionoo.torproject.org/details?search=" + nickname)
    response = r.json()
    i = response["relays"][0]
    if (
        i["nickname"].casefold() == nickname.casefold()
        or i["fingerprint"] == nickname.upper()
        or i["or_addresses"][0].split(":")[0] == nickname
    ):
        if i["running"] == False:
            status = ":red_circle:"
            color = 0xE74C3C
            description = "This relay is offline."
        elif "overload_general_timestamp" in i:
            status = ":yellow_circle:"
            color = 0xF1C40F
            description = "This relay is overloaded."
        else:
            status = ":green_circle:"
            color = 0x2ECC71
            description = "This relay is running."
        embed = discord.Embed(
            title=f"{status} {i['nickname']}", description=description, color=color
        )
        embed.add_field(
            name="First Seen",
            value=f"{i['first_seen'][:10]} ({days_between(i['first_seen'], datetime.now())} ago) ",
            inline=False,
        )
        embed.add_field(
            name="Uptime",
            value=f"{days_between(i['last_restarted'], datetime.now())}",
            inline=False,
        )
        embed.add_field(
            name="Country",
            value=f":flag_{i['country']}: {i['country_name']}",
            inline=False,
        )
        embed.add_field(
            name="Flags", value=" ".join(change_flags(i["flags"])), inline=False
        )
        embed.add_field(name="Platform", value=i["platform"], inline=False)
        embed.add_field(name="Fingerprint", value=i["fingerprint"], inline=False)
        embed.add_field(name="OR Address", value=i["or_addresses"][0], inline=False)
        if "contact" in i:
            embed.add_field(name="Contact Info", value=i["contact"], inline=False)
        else:
            embed.add_field(name="Contact Info", value="none", inline=False)
        embed.add_field(
            name="Consensus Weight", value=i["consensus_weight"], inline=False
        )
        embed.add_field(
            name="Metrics", value=f"https://metrics.torproject.org/rs.html#details/{i['fingerprint']}", inline=False
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error", description="No relay found!", color=0xE74C3C
        )
        await ctx.send(embed=embed)
@bot.command()
async def tor_bridge(ctx, nickname):
    await ctx.channel.trigger_typing()
    r = requests.get("https://onionoo.torproject.org/details?search=" + nickname)
    response = r.json()
    i = response["bridges"][0]
    if (
        i["nickname"].casefold() == nickname.casefold()
        or i["hashed_fingerprint"] == nickname.upper()
    ):
        if i["running"] == False:
            status = ":red_circle:"
            color = 0xE74C3C
            description = "This bridge is offline."
        elif "overload_general_timestamp" in i:
            status = ":yellow_circle:"
            color = 0xF1C40F
            description = "This bridge is overloaded."
        else:
            status = ":green_circle:"
            color = 0x2ECC71
            description = "This bridge is running."
        iplist = []
        for i2 in i['or_addresses']:
            if re.match('.', i2):
                if 'IPv4' in iplist:
                    continue
                else:
                    iplist.append('IPv4')
            if re.match(':', i2):
                if 'IPv6' in iplist:
                    continue
                else:
                    iplist.append('IPv6')
        embed = discord.Embed(
            title=f"{status} {i['nickname']}", description=description, color=color
        )
        embed.add_field(
            name="First Seen",
            value=f"{i['first_seen'][:10]} ({days_between(i['first_seen'], datetime.now())} ago) ",
            inline=False,
        )
        embed.add_field(
            name="Uptime",
            value=f"{days_between(i['last_restarted'], datetime.now())}",
            inline=False,
        )
        embed.add_field(
            name="Flags", value=" ".join(change_flags(i["flags"])), inline=False
        )
        embed.add_field(name="Platform", value=i["platform"], inline=False)
        embed.add_field(name="Fingerprint", value=i["hashed_fingerprint"], inline=False)
        embed.add_field(name="OR Address", value=" ".join(iplist), inline=False)
        embed.add_field(name="Transport Protocols", value=" ".join(i["transports"]), inline=False)
        embed.add_field(name="Bridge Distrubition", value=i["bridgedb_distributor"], inline=False)
        embed.add_field(
            name="Metrics", value=f"https://metrics.torproject.org/rs.html#details/{i['hashed_fingerprint']}", inline=False
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error", description="No bridge found!", color=0xE74C3C
        )
        await ctx.send(embed=embed)

bot.run(token)
