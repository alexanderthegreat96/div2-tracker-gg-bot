import mysql.connector
import time
from classes import BotConfiguration

class Database:
    def __init__(self):
        config = BotConfiguration.BotConfiguration()
        self.connection = mysql.connector.connect(
            host=config.mysqlHost(),
            database=config.mysqlDb(),
            user=config.mysqlUser(),
            password=config.mysqlPass(),
        )
        self.cursor = self.connection.cursor()
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def listLogs(self):
        self.cursor.execute(
            "SELECT id,discord_username,playername,created_at FROM logs ORDER BY created_at")
        result = self.cursor.fetchall()
        if (result):
            return result
        else:
            return 'No data found'

    def saveToDatabase(self,query, discord_username, platformUserId, platformUsername, timePlayedTotal, timePlayedPve,
                       timePlayedInDarkZone, killsPvP, killsHeadshot,
                       headshots, timePlayedRogue, timePlayedRogueLongest, roguesKilled, killsNpcs):

        logSql = "INSERT into logs (discord_username,playername,platformid,created_at) VALUES (%s,%s,%s,%s)"
        logVal = (discord_username, platformUsername, platformUserId, self.now)
        self.cursor.execute(logSql, logVal)
        self.connection.commit()

        checkQuery = self.cursor.execute(
            'SELECT id FROM stats WHERE username = "' + platformUsername + '" AND identifier = "' + platformUserId + '"')
        result = self.cursor.fetchone()
        if (result):
            id = result[0]
            updateStatsSql = 'UPDATE stats SET timePlayed = "%s",timePlayedDarkZone = "%s",killsPvP = "%s",killsHeadshot  = "%s",headshots  = "%s",timePlayedRogue  = "%s",timePlayedRogueLongest = "%s",roguesKilled = "%s",killsNpc = "%s",timePlayedPve = "%s" WHERE id ="%s"'
            updateStatsVals = (
            timePlayedTotal, timePlayedInDarkZone, killsPvP, killsHeadshot, headshots, timePlayedRogue,
            timePlayedRogueLongest, roguesKilled, killsNpcs, timePlayedPve, id)
            self.cursor.execute(updateStatsSql, updateStatsVals)
            self.connection.commit()
        else:
            statsSql = "INSERT into stats (username,identifier,timePlayed,timePlayedDarkZone,killsPvP,killsHeadshot,headshots,timePlayedRogue,timePlayedRogueLongest,roguesKilled,killsNpc,timePlayedPve,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            statsVals = (
            platformUsername, platformUserId, timePlayedTotal, timePlayedInDarkZone, killsPvP, killsHeadshot, headshots,
            timePlayedRogue,
            timePlayedRogueLongest, roguesKilled, killsNpcs, timePlayedPve, self.now)
            self.cursor.execute(statsSql, statsVals)
            self.connection.commit()
        # disconnecting from server
        self.connection.close()


    def searchHistory(self,username):
        self.cursor.execute(
            "SELECT playername,platformid,created_at FROM logs WHERE discord_username ='" + username + "' ORDER BY created_at DESC LIMIT 10")

        result = self.cursor.fetchall()

        output = ""
        if (result):
            output += "Your last 10 seaches: \n"
            for playername, platformid, created_at in result:
                output += "``` - " + playername + " (" + platformid + ") (" + str(created_at) + ")```"
        else:
            output += "You have no search history for this username."
        return output