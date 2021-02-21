from discord.ext import commands
import discord

thumbsUp = '\N{THUMBS UP SIGN}'
xButton = '❌'

class Homework(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.user = None

    #!dm command
    @commands.command()
    async def dm(self, ctx):
        message = await ctx.send('React to get a cool dm')
        await message.add_reaction(thumbsUp)
        self.message = message
        print('frnfrnjifrn')


    @commands.Cog.listener()
    #reaction listener
    async def on_reaction_add(self, reaction, user):
        print(user)
        #user reacts to bot in channel and is not bot
        if not user.bot and reaction.emoji == thumbsUp:
            message1 = await user.send("Hi, send your homework file below or react with the x button to cancel the operation")
            await message1.add_reaction(xButton)
            self.user = user
        #user reacts X in dm and its not bot
        if reaction.emoji == xButton and not user.bot:
            await user.send("Hand-in cancelled")
    
    @commands.Cog.listener()
    #message listener        
    async def on_message(self, message):
        if not message.guild and message.author == self.user:
            await message.channel.send('this is a dm')