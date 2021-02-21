from discord.ext import commands
import discord
from datetime import datetime
from collections import OrderedDict

#consts
thumbsUp = '\N{THUMBS UP SIGN}'
xButton = '❌'
nReacts = [
    '1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣'
]
ico = "https://cdn.discordapp.com/attachments/808832489459023913/813049155957424168/unknown.png"

class ACommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #"command":"desc"
        self.commands = OrderedDict()
        self.commands['hmw'] = "Create a homework assignment"
        self.commands['openGroup #'] = "Open the voice channel of specified group (# = group number)"
        self.commands['closeGroup #'] = "Close the voice channel of specified group (# = group number)"
        self.messageActions = None

    #sends the menu in ctx if ctx is channel actions
    async def ShowCommands(self, ctx):
        if ctx.channel.name == "actions":
            strDsc = "React to one of the presented options to initiate the command"
            embedActions = discord.Embed(title="Available Actions", description=strDsc, color=0xe0d122)
            embedActions.set_thumbnail(url=ico)
            i = 0
            for cmdName, cmdDsc in self.commands.items():
                embedActions.add_field(name="!"+cmdName, value=nReacts[i] + " :" + cmdDsc + "\n\n\n", inline=False)
                i+=1
            self.messageActions = await ctx.channel.send(embed=embedActions)
            i=0
            for cmdName in self.commands.items():
                await self.messageActions.add_reaction(nReacts[i])
                i+=1
            
    @commands.command()
    async def actions(self, ctx):
        await self.ShowCommands(ctx)
    
    @commands.Cog.listener()
    #reaction listener
    async def on_reaction_add(self, reaction, user):
        if reaction.message == self.messageActions and not user.bot:
            index = nReacts.index(reaction.emoji)
            command = list(self.commands.items())[index][0]
            print(command)
            found = False
            for cmd in self.bot.commands:
                print(cmd)
                if cmd.name == command: 
                    found = True
                    break 
                else: continue
            if found == False:
                await reaction.message.channel.send(xButton + " incorrect bot command provided")
            else:
                await cmd.__call__(reaction.message.channel)

            
