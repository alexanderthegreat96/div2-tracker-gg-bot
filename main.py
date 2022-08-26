__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "beta"

import requests
import time
import json
from discord.ext import commands

#https://tracker.gg/developers/apps/
trackergg_api_key = ''
#https://discord.com/developers/applications/yourappkey/bot
botToken = ''

## Grabs data from trackergg

def returnPlayerStats(playername):
    apiUrl = f'https://public-api.tracker.gg/v2/division-2/standard/profile/uplay/{playername}'
    apiHeaders = {'TRN-Api-Key': trackergg_api_key}
    response = requests.get(apiUrl,apiHeaders)

    if(response.status_code == 200):
        return response.json()
    else:
        return response.json

def playerInfo(playername):
    response = json.dumps(returnPlayerStats(playername))
    response = json.loads(response)

    if(response['data']):
        platformInfo = response['data']['platformInfo']
        playerStats = response['data']['segments'][0]['stats']

        output = platformInfo['avatarUrl'] + '\n'
        output += '```'
        output += 'Displaying player stats: \n'


        output += 'Platform: ' + platformInfo['platformSlug']+ '\n'
        output += 'Username: ' + platformInfo['platformUserIdentifier']+ '\n'

        for j in playerStats:
            output += playerStats[j]['displayName'] + ' : ' + playerStats[j]['displayValue'] + "\n"

        output += '```'
        return output
    else:
        return 'No stats found!'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def shd(ctx, arg):
    print('Sending command: ' + arg)
    start_time = round(time.time() * 1000)
    if arg.lower() == "help":
        await ctx.channel.send("Get player stats: !shd <player_name>\nBot ping test: !shd ping")
    elif arg.lower() == "ping":
        end_time = round(time.time() * 1000)
        await ctx.channel.send("pong (%s ms)" % str(end_time - start_time))
    else:
        try:
            parser = playerInfo(arg)
            await ctx.channel.send(parser)
        except (TypeError, KeyError):
            await ctx.channel.send("Player does not exist!")


if __name__ == '__main__':
    print('Bot is running. Awaiting !shd command input: \n')
    bot.run(botToken) # Include token here.

   
