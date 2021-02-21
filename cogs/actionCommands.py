from discord.ext import commands
import discord
from datetime import datetime

thumbsUp = '\N{THUMBS UP SIGN}'
xButton = '❌'

class ACommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        return