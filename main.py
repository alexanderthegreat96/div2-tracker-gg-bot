__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "beta"

import asyncio
import time
from discord.ext import commands
import discord
from classes.DataGrabber import DataGrabber
from classes.Database import Database
from classes.BotConfiguration import BotConfiguration


bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@bot.command()
async def dth(ctx, arg, arg2 = ''):
    user_id = format(ctx.message.author.id)
    username = ctx.message.author.name
    discord_name = ctx.message.guild.name

    print(username + ' from '+discord_name+' is sending command: ' + arg)

    start_time = round(time.time() * 1000)
    if arg.lower() == "hello":
        await ctx.channel.send(
            "Hello, " + username + " \nI am a bot built by a division2 enthusiat. I can help you search for player stats using ```/dth <usernamehere>``` \n")
        await ctx.channel.send(
            "Use ```/dth history``` to check your search history \n")
        await asyncio.sleep(10)
    elif arg.lower() == "help":
        await ctx.channel.send("Hi, " + username + ". You can search for player stats using ```/dth username123``` and view your history with ``` /dth history ``` ")
        await asyncio.sleep(10)
    elif arg.lower() == "history":
        database = Database()
        await ctx.channel.send(database.searchHistory(username))
        await asyncio.sleep(10)
    else:
        await ctx.channel.send("Querying data, please wait...")
        try:
            grabber = DataGrabber(arg, username)
            playerStats = grabber.playerInfo()

            await ctx.channel.send(playerStats)
            await asyncio.sleep(10)
        except (TypeError, KeyError):
            await ctx.channel.send("Player does not exist!")
            await asyncio.sleep(10)


if __name__ == '__main__':
    print('DTH-Public-Bot is running. Awaiting /dth command input: \n')
    config = BotConfiguration()
    bot.run(config.botToken())  # Include token here.
