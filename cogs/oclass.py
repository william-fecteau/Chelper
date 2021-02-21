from discord.ext import commands
from discord import utils

import datetime

class OClass(commands.Cog):
    def __init__(self, bot, dicGuilds):
        self.bot = bot

        self.dicGuilds = dicGuilds

        self.daysOfWeek = ["sunday", "tuesday", "wednesday", "thursday", "friday", "saturday", "monday"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild != None and not message.author.bot and message.channel.name[:-1] == "control-":
            nbChannel = message.channel.name[-1]
            cTeacherZone = utils.get(message.guild.categories, name="Teacher-zone")
            tcCurGroup = utils.get(cTeacherZone.text_channels, name="control-{}".format(nbChannel))

            day, hour = message.content.lower().split(" ")
            start, finish = hour.split("-")

            startH, startM = start.split("h")
            finishH, finishM = finish.split("h")

            datetime = datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)

            ##self.dicGuilds[message.guild.id]["classes"]["group-"+str(nbChannel)][day] = 
                
    @commands.command()
    async def opengroup(self, ctx, groupNum : int):
        pass

    @commands.command()
    async def closegroup(self, ctx, groupNum: int):
        pass
                
