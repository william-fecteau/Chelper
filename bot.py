import os
import sys

#import discord
from discord.ext import commands
from discord import utils

from cogs import *
from db.dbo import DBO
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='!')

dicGuilds = dict()

categoriesName = ["Verification", "Teacher-update", "Teacher-zone", "Student-zone"]
textChannelsName = {
    "Verification": ["verification"],
    "Teacher-update": ["actions"],
    "Teacher-zone": [],
    "Student-zone": [],
}

hardcodedStudents = [{"id": "1835343", "firstName": "William", "lastName": "Fecteau"}]


@bot.event
async def on_ready():
    for guild in bot.guilds:
        await InitServer(guild)


@bot.event
async def on_guild_join(guild):
    await InitServer(guild)
    
    # Creating the first text channel (#actions)
    cTeacherUpdate = utils.get(guild.categories, name="Teacher-update")
    tcAction = utils.get(cTeacherUpdate.text_channels, name="actions")

    dicGuilds[guild.id]["isCreating"] = True
    dicGuilds[guild.id]["step"] = 0
    await tcAction.send("Hi! What is the name of your class?")

@bot.event
async def on_message(message):
    cTeacherUpdate = utils.get(message.guild.categories, name="Teacher-update")

    # If server is in is-creating mode and that the message was sent in actions from the teacher
    if dicGuilds[message.guild.id]["isCreating"] and message.channel == utils.get(cTeacherUpdate.text_channels, name="actions") and not message.author.bot:
        if dicGuilds[message.guild.id]["step"] == 0:
            await message.guild.edit(name = message.content)
            dicGuilds[message.guild.id]["step"] += 1
            await message.channel.send("How many groups would you like to create?")
        elif dicGuilds[message.guild.id]["step"] == 1:
            try:
                for i in range (int(message.content)):
                    tempCategorie= utils.get(message.guild.categories, name="Teacher-zone")
                    await tempCategorie.create_text_channel("Assignments of group " + str(i+1))
                    tempCategorie= utils.get(message.guild.categories, name="Student-zone")
                    await tempCategorie.create_text_channel("Group " + str(i+1))
                    await tempCategorie.create_voice_channel("Group " +  str(i+1))
                    await message.guild.create_role(name="Group" +  str(i+1))
            except:
                message.channel.send("Please use a valid integer")




async def InitServer(guild):
    dicGuilds[guild.id] = {}

    dicGuilds[guild.id]["isCreating"] = False

    for categoryName in categoriesName:
        # Creating category
        curCategory = utils.get(guild.categories, name=categoryName)
        if curCategory == None:
            curCategory = await guild.create_category_channel(categoryName)
        
        # Creating text channels for this category
        for tcName in textChannelsName[categoryName]:
            curTextChannel = utils.get(curCategory.text_channels, name=tcName)
            if not curTextChannel:
                curTextChannel = await curCategory.create_text_channel(tcName)

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
    bot.add_cog(inscription.Inscription(bot, dicGuilds))
    bot.add_cog(oclass.OClass(bot))
    bot.add_cog(homework.Homework(bot))

    bot.run(TOKEN)
