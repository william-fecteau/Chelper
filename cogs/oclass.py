from discord.ext import commands
from discord import utils

class OClass(commands.Cog):
    def __init__(self, bot, dicGuilds):
        self.bot = bot

        self.dicGuilds = dicGuilds

        self.daysOfWeek = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.channel.name[:-1] == "control-group-":
            nbChannel = message.channel.name[-1]
            cTeacherZone = utils.get(message.guild.categories, name="Teacher-zone")
            tcCurGroup = utils.get(cTeacherZone.text_channels, name="control-group-"+str(nbChannel))

            day, hour = message.content.lower().split(" ")
            start, finish = hour.split("-")

            startH, startM = start.split("h")
            finishH, finishM = finish.split("h")
                
                
