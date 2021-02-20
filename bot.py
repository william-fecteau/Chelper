import os
import sys

#import discord
from discord.ext import commands

from cogs import *
from db.dbo import DBO
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='!')

@bot.command()
async def booga(ctx, arg1):
    await ctx.send('You passed {}'.format(arg1))


if __name__ == '__main__':
    # .ENV loading
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')

    # DB connection
    dbo = DBO(DB_SERVER, DB_NAME)
    dbo.testSelect()

    # Loading cogs
    bot.add_cog(test.Test(bot))

    bot.run(TOKEN)
