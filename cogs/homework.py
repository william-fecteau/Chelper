from discord.ext import commands
import discord
from datetime import datetime

thumbsUp = '\N{THUMBS UP SIGN}'
xButton = '❌'

class Homework(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.user = None
        self.channelHandIn = None
        self.waitingForFile = False


    #!dm command
    @commands.command()
    async def dm(self, ctx):
        strDsc = "React to this message with "+ thumbsUp +" if you are ready to hand in your homework"
        embedfield = discord.Embed(title="Homework handing out", description=strDsc, color=0xe0d122)
        embedfield.add_field(name="Due date:", value=datetime.today().strftime('%Y-%m-%d-%H:%M'), inline=False)
        message = await ctx.send(embed=embedfield)
        await message.add_reaction(thumbsUp)
        self.message = message
        self.channelHandIn = discord.utils.get(ctx.guild.channels, name='homework-hand-in')


    @commands.Cog.listener()
    #reaction listener
    async def on_reaction_add(self, reaction, user):
        print(user)
        #user reacts to bot in channel and is not bot
        if not user.bot and reaction.emoji == thumbsUp:
            message1 = await user.send("Hi, send your homework file below or react with the x button to cancel the operation, add a note by sending your file with a message")
            self.user = user
            await message1.add_reaction(xButton)
            self.waitingForFile = True
        #user reacts X in dm and its not bot
        if reaction.emoji == xButton and not user.bot and self.waitingForFile:
            await user.send("Hand-in cancelled")
            self.waitingForFile = False
    
    @commands.Cog.listener()
    #message listener        
    async def on_message(self, message):
        #bot is waiting for a file and message is not in server (dms) and the sender isn't the bot
        if self.waitingForFile and not message.guild and not message.author.bot:
            #file present with message
            if message.attachments:
                embedLog = discord.Embed(title="Homework received", description=datetime.today().strftime('%Y-%m-%d-%H:%M'), color=0x00ff00)
                embedLog.add_field(name="Student: ", value=message.author.display_name, inline=False)
                #if message has somethign written with it
                if message.content:
                    embedLog.add_field(name="Student's note: ", value=message.content, inline=False)
                embedLog.add_field(name="File: ", value=message.attachments[0].url, inline=False)
                await self.channelHandIn.send(embed=embedLog)
                await message.channel.send("File uploaded successfully!")
                self.waitingForFile = False
            #no files attached
            else: await message.channel.send("No file sent")