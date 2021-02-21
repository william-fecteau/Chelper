import os
import sys

import discord
from discord.ext import commands
from discord import utils

from cogs import *
from db.dbo import DBO
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

dicGuilds = dict()

categoriesName = ["Verification", "Teacher-update", "Teacher-zone", "Student-zone"]
textChannelsName = {
    "Verification": ["verification"],
    "Teacher-update": ["actions"],
    "Teacher-zone": ["homework-hand-in"],
    "Student-zone": [],
}

hardcodedStudents = {"1835343": {"group": 1, "firstName": "William", "lastName": "Fecteau"}}
registredStudents = []

@bot.event
async def on_ready():
    for guild in bot.guilds:
        # TODO dicGuilds should come from DB
        dicGuilds[guild.id] = {}

        # TODO: FOR TESTING REMOVE LATER
        dicGuilds[guild.id]["nbGroup"] = 2
        dicGuilds[guild.id]["isCreating"] = False

        await InitServer(guild)


@bot.event
async def on_guild_join(guild):
    for channel in guild.channels:
        await channel.delete()
    
    # Creating the first text channel (#actions)
    cTeacherUpdate = utils.get(guild.categories, name="Teacher-update")
    if cTeacherUpdate == None:
        cTeacherUpdate = await guild.create_category_channel("Teacher-update")

    tcAction = utils.get(cTeacherUpdate.text_channels, name="actions")
    if tcAction == None:
        tcAction = await cTeacherUpdate.create_text_channel("actions")

    dicGuilds[guild.id] = {}
    dicGuilds[guild.id]["isCreating"] = True
    dicGuilds[guild.id]["step"] = 0
    await tcAction.send("Hi! What is the name of your class?")

@bot.event
async def on_message(message):
    if not message.content.startswith('!') and message.guild != None and message.guild.id in dicGuilds:
        cTeacherUpdate = utils.get(message.guild.categories, name="Teacher-update")

        # If server is in is-creating mode and that the message was sent in actions from the teacher
        if dicGuilds[message.guild.id]["isCreating"] and message.channel == utils.get(cTeacherUpdate.text_channels, name="actions") and not message.author.bot:   
            if dicGuilds[message.guild.id]["step"] == 0:
                await message.guild.edit(name = message.content)
                dicGuilds[message.guild.id]["step"] += 1
                await message.channel.send("How many groups would you like to create?")
            elif dicGuilds[message.guild.id]["step"] == 1:
                nb = -1
                valid = True
                try:
                    nb = int(message.content)
                except:
                    await message.channel.send("Please use a valid integer")
                    valid = False

                if nb > 0:
                    dicGuilds[message.guild.id]["nbGroup"] = nb
                    dicGuilds[message.guild.id]["step"] += 1

                    await InitServer(message.guild)

                    # Sending next message in control channels
                    cTeacherZone = utils.get(message.guild.categories, name="Teacher-zone")
                    for i in range(1, dicGuilds[message.guild.id]["nbGroup"] + 1):
                        tcCurGroup = utils.get(cTeacherZone.text_channels, name="control-{}".format(i))
                        await tcCurGroup.send("When is your class with the group {}? (Ex: Thursday 8h15-10h15)".format(i))
                    
                    # TODO: A Welcome message that presents every channel

                    await message.channel.send("Almost done! Please look in your control channel to setup your class schedule with each group :)")
                elif valid:
                    await message.channel.send("Please use a number greater than 0")

    else:
        await bot.process_commands(message)



async def InitServer(guild):
    # TODO: dicGuilds should come from DB
    dicGuilds[guild.id]["students"] = hardcodedStudents
    dicGuilds[guild.id]["registredStudents"] = registredStudents

    for categoryName in categoriesName:
        # Creating category
        curCategory = utils.get(guild.categories, name=categoryName)
        if curCategory == None:
            curCategory = await guild.create_category_channel(categoryName)
        
        # By default, we hide every category for default user
        await curCategory.set_permissions(guild.default_role, read_messages=False, send_messages=False)

        # Creating text channels for this category
        for tcName in textChannelsName[categoryName]:
            curTextChannel = utils.get(curCategory.text_channels, name=tcName)
            if not curTextChannel:
                curTextChannel = await curCategory.create_text_channel(tcName)

            # By default, we hide every text channel for default user
            await curTextChannel.set_permissions(guild.default_role, read_messages=False, send_messages=False)

    # Creating channels for all the groups
    cVerification = utils.get(guild.categories, name="Verification")
    for i in range(1, dicGuilds[guild.id]["nbGroup"] + 1):
        control_channel_name = "control-{}".format(i)
        group_channel_name = "group-{}".format(i)

        cTeacherZone = utils.get(guild.categories, name="Teacher-zone")
        tcControl = utils.get(cTeacherZone.text_channels, name=control_channel_name)
        if tcControl == None: 
            ctrlChannel = await cTeacherZone.create_text_channel(control_channel_name)

        cStudentZone = utils.get(guild.categories, name="Student-zone")
        tcGroup = utils.get(cStudentZone.text_channels, name=group_channel_name)
        if tcGroup == None:
            tcGroup = await cStudentZone.create_text_channel(group_channel_name)
        vcGroup = utils.get(cStudentZone.voice_channels, name=group_channel_name)
        if vcGroup == None:
            vcGroup = await cStudentZone.create_voice_channel(group_channel_name)

        role = utils.get(guild.roles, name=group_channel_name)
        if role == None:
            groupRole = await guild.create_role(name=group_channel_name)
            await cVerification.set_permissions(groupRole, read_messages=False, send_messages=False)
            await tcGroup.set_permissions(groupRole, read_messages=True, send_messages=True)
            await vcGroup.set_permissions(groupRole, read_messages=True, send_messages=True)


    # ======================== Specific permissions ========================
    # - Verification must be accessible for every user on login
    cVerification = utils.get(guild.categories, name="Verification")
    await cVerification.set_permissions(guild.default_role, read_messages=True, send_messages=True)
    for channel in cVerification.text_channels:
        await channel.set_permissions(guild.default_role, read_messages=True, send_messages=True)
            


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
    bot.add_cog(oclass.OClass(bot, dicGuilds))
    bot.add_cog(homework.Homework(bot))

    bot.run(TOKEN)
