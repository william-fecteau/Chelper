from discord.ext import commands
from discord import utils

class OClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.dicGuilds = {}

