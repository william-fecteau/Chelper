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
            message1 = await user.send("Hi, send your homework file below or react with the x button to cancel the operation")
            self.user = user
            await message1.add_reaction(xButton)
        #user reacts X in dm and its not bot
        if reaction.emoji == xButton and not user.bot:
            await user.send("Hand-in cancelled")
    
    @commands.Cog.listener()
    #message listener        
    async def on_message(self, message):
        if not message.guild and message.author == self.user:
            print(message.author)
            embedLog = discord.Embed(title="Homework received", description=datetime.today().strftime('%Y-%m-%d-%H:%M'), color=0x00ff00)
            embedLog.add_field(name="Student: ", value=message.author.display_name, inline=False)
            embedLog.add_field(name="File: ", value=message.attachments[0].url, inline=False)
            await self.channelHandIn.send(embed=embedLog)
            await message.channel.send("File uploaded successfully!")