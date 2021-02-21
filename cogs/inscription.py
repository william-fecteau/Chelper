from discord.ext import commands
from discord import utils

class Inscription(commands.Cog):
    def __init__(self, bot, dicGuilds):
        self.bot = bot
        self.dicGuilds = dicGuilds

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cVerification = utils.get(member.guild.categories, name="Verification")
        tcVerification = utils.get(cVerification.text_channels, name="verification")

        await tcVerification.send("To verifiy your identity, please enter your ID number in this chat (Don't worry, nobody will see it ;) )")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            cVerification = utils.get(message.guild.categories, name="Verification")
            
            # Si la catégorie existe
            if cVerification != None:

                # Récupération du channel
                tcVerification = utils.get(cVerification.text_channels, name="verification")
                if tcVerification != None and tcVerification == message.channel:
                    msg = "This is not a valid id"
                    if message.content in self.dicGuilds[message.guild.id]["students"]:
                        student = self.dicGuilds[message.guild.id]["students"][message.content]

                        await message.author.edit(nick="{} {}".format(student["firstName"], student["lastName"]))
                        msg = "Hi {} {}! Your account is now validated".format(student["firstName"], student["lastName"])

                        roleName = "Group" + str(student["group"])
                        await message.author.add_roles(utils.get(message.guild.roles, name=roleName))
                        
                        self.dicGuilds[message.guild.id]["registredStudents"].append(student)
                        del self.dicGuilds[message.guild.id]["students"][message.content]

                    await tcVerification.send(msg)
                    await message.delete()



    