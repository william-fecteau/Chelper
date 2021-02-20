from discord.ext import commands

class Inscription(commands.Cog):
    def __init__(self, bot, dicGuilds):
        self.bot = bot
        self.dicGuilds = dicGuilds

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("yaho")