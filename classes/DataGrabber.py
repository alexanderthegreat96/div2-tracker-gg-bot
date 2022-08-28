from selenium import webdriver
from bs4 import BeautifulSoup
import json
from classes import Database

class DataGrabber:
    def __init__(self,playername, username):
        self.playername = playername
        self.username = username
        self.database = Database.Database()
    def filterUsernames(self):
        f = open('whitelist.json')
        data = json.load(f)
        return data['filter_names']

    def playerInfo(self):

        whitelist = self.filterUsernames()

        if(self.playername not in whitelist):

            browser = webdriver.Chrome(executable_path="bin\chromedriver.exe")
            browser.get('https://api.tracker.gg/api/v2/division-2/standard/profile/uplay/' + self.playername)
            soup = BeautifulSoup(browser.page_source, features="html.parser")
            bodyText = soup.find("body").text
            if (bodyText):
                jsonBody = bodyText
                response = json.loads(jsonBody)

                if ("errors" in response):
                    return response['errors'][0]['message']
                else:
                    platformInfo = response['data']['platformInfo']
                    playerStats = response['data']['segments'][0]['stats']

                    platformUserId = platformInfo['platformUserId']
                    platformUsername = platformInfo['platformUserIdentifier']
                    platformAvatar = platformInfo['avatarUrl']
                    timePlayedTotal = playerStats['timePlayed']['displayValue']
                    timePlayedPve = playerStats['timePlayedPve']['displayValue']
                    timePlayedInDarkZone = playerStats['timePlayedDarkZone']['displayValue']
                    killsPvP = playerStats['killsPvP']['displayValue']
                    killsHeadshot = playerStats['killsHeadshot']['displayValue']
                    headshots = playerStats['headshots']['displayValue']
                    timePlayedRogue = playerStats['timePlayedRogue']['displayValue']
                    timePlayedRogueLongest = playerStats['timePlayedRogueLongest']['displayValue']
                    roguesKilled = playerStats['roguesKilled']['displayValue']
                    killsNpcs = playerStats['killsNpc']['displayValue']

                    isSuspicious = response['data']['userInfo']['isSuspicious']
                    isInfluencer = response['data']['userInfo']['isInfluencer']

                    if (not isSuspicious):
                        isSuspicious = 'No'

                    if (not isInfluencer):
                        isInfluencer = 'No'

                    output = platformAvatar + '\n'
                    output += '```'

                    output += 'Platform UID (never changes): ' + platformUserId + '\n'
                    output += 'Username: ' + platformUsername + '\n'
                    output += 'Is suspicious  : ' + isSuspicious + '\n'
                    output += 'Is influencer  : ' + isInfluencer + '\n'
                    output += 'Time played in total : ' + ' : ' + timePlayedTotal + '\n'
                    output += 'Time spent in the Dark Zone : ' + ' : ' + timePlayedInDarkZone + '\n'
                    output += 'Time spent in PVE :' + ' : ' + timePlayedPve + '\n'
                    output += 'Total PVP Kills: ' + killsPvP + '\n'
                    output += 'Headshot Kills: ' + killsHeadshot + '\n'
                    output += 'Total Headshots: ' + ' : ' + headshots + '\n'
                    output += 'Rogue Time Played : ' + ' : ' + timePlayedRogue + '\n'
                    output += 'Rogue Longest Time Played' + ' : ' + timePlayedRogueLongest + '\n'
                    output += 'Rogue Killed : ' + ' : ' + roguesKilled + '\n'
                    output += 'NPC Kills: ' + ' : ' + killsNpcs + '\n'
                    output += '```'

                    ##beging saving data to the database##

                    self.database.saveToDatabase(self.playername, self.username, platformUserId, platformUsername, timePlayedTotal, timePlayedPve,
                                   timePlayedInDarkZone, killsPvP, killsHeadshot,
                                   headshots, timePlayedRogue, timePlayedRogueLongest, roguesKilled, killsNpcs)

                    return output
            else:
                return 'Unable to parse json output from https://api.tracker.gg/api/v2/division-2/standard/profile/uplay/' + self.playername
        else:
            return 'No data found.'