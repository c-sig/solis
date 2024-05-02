import discord
import requests
from discord.ext import commands

VERIFICATION = 1228306638574981120
APPROVAL = 1112590492920713216
ROLE_ID = 1226182521239244850
GUILD_ID = 1093029794406465596

class VerificationView(discord.ui.View):
    def __init__(self, bot: discord.Bot, user_id: int, content: str, approval_request, reply):
        super().__init__(timeout=None)
        self.bot = bot
        self.user_id = user_id
        self.content = content
        self.approval_request = approval_request
        self.reply = reply
        
    @discord.ui.button(label="Verify", row=0, style=discord.ButtonStyle.green)
    async def verify_callback(self, button, interaction):
        applicant = self.bot.get_user(self.user_id)
        guild = self.bot.get_guild(GUILD_ID)
        member = guild.get_member(self.user_id)
        
        role = guild.get_role(ROLE_ID)
        await member.add_roles(role)
        
        await member.edit(nick=self.content)
        
        await interaction.response.edit_message(view=None)
        
        embed = discord.Embed(title="Application approved!", description="Thank you for applying! Please get your roles in the server to get started! Bridgewatch on top!", color=0x00ff00)
        
        try:
            await applicant.send(embed=embed)
        finally:
            pass
        
        await self.approval_request.delete()
        await self.reply.delete()
            
    @discord.ui.button(label="Wrong Screenshot", row=1, style=discord.ButtonStyle.red)
    async def reject_callback(self, button, interaction):
        applicant = self.bot.get_user(self.user_id)
        await interaction.response.edit_message(view=None)
        
        embed = discord.Embed(title="Application rejected!",
                              description="Please fix your screenshot before reapplying! Follow the example screenshot.", color=0xff0000)
        try:
            await applicant.send(embed=embed)
        except:
            pass
        
        await self.approval_request.delete()
        await self.reply.delete()  
            
    @discord.ui.button(label="Rank Too Low", row=2, style=discord.ButtonStyle.red)  
    async def rank_callback(self, button, interaction):
        applicant = self.bot.get_user(self.user_id)
        await interaction.response.edit_message(view=None)
        
        embed = discord.Embed(title="Application rejected!",
                              description="Your rank is too low! Please play for Bridgewatch more before reapplying!", color=0xff0000)
        try:
            await applicant.send(embed=embed)
        except:
            pass
        
        await self.approval_request.delete()
        await self.reply.delete()
            
    @discord.ui.button(label="Wrong Username", row=3, style=discord.ButtonStyle.red)
    async def username_callback(self, button, interaction):
        applicant = self.bot.get_user(self.user_id)
        await interaction.response.edit_message(view=None)
        
        embed = discord.Embed(title="Application rejected!",
                              description="Please use your OWN username! Do not use other people's username!", color=0xff0000)
        try:
            await applicant.send(embed=embed)
        except:
            pass
        
        await self.approval_request.delete()
        await self.reply.delete()        
            
class Verify(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        verification_channel = self.bot.get_channel(VERIFICATION)
        approval_channel = self.bot.get_channel(APPROVAL)
        
        if message.author == self.bot.user:
            return
        
        if message.channel.id != VERIFICATION:
            return
        
        if not message.attachments:
            embed = discord.Embed(title="Missing screenshot!", description=f"{message.author.mention} Please send your screenshot in the same message as your username!", color=0xff0000)
            reply = await verification_channel.send(embed=embed)
            await message.delete(delay=3600)
            await reply.delete(delay=3600)
            return
        
        if not message.content:
            embed = discord.Embed(title="Missing username!", description=f"{message.author.mention} Please send your username in the same message as your screenshot!", color=0xff0000)
            reply = await verification_channel.send(embed=embed)
            await message.delete(delay=3600)
            await reply.delete(delay=3600)
            return
        
        if not message.content.isalnum():
                embed = discord.Embed(title="Invalid username!",
                                      description=f"{message.author.mention} Please send ONLY your username in the same message as your screenshot! Do not include 'Register', 'IGN:', or anything other than your actual username!",
                                      color=0xff0000)
                reply = await verification_channel.send(embed=embed)
                await message.delete(delay=3600)
                await reply.delete(delay=3600)
                return
            
        url = f"https://gameinfo-sgp.albiononline.com/api/gameinfo/search?q={message.content}"
        response = requests.get(url)
        data = response.json()
        
        try:
            player = data['players'][0]
            player_name = player['Name']
            if message.content != player_name:
                embed = discord.Embed(title="Invalid username!",
                                      description=f"{message.author.mention} Please send your ACTUAL username in the same message as your screenshot! Please note that this is CaSe SeNsItIvE. csig is not cSig, CsiG, etc.",
                                      color=0xff0000)
                reply = await verification_channel.send(embed=embed)
                await message.delete(delay=3600)
                await reply.delete(delay=3600)
                return
        except:
            embed = discord.Embed(title="Invalid username!",
                                  description=f"{message.author.mention} Please send your ACTUAL username in the same message as your screenshot! Please note that this is CaSe SeNsItIvE. csig is not cSig, CsiG, etc.",
                                  color=0xff0000)
            reply = await verification_channel.send(embed=embed)
            await message.delete(delay=3600)
            await reply.delete(delay=3600)
            return
        
        embed = discord.Embed(title="Application received!", description=f"{message.author.mention} Please wait for staff to review your application!", color=0x00ff00)
        
        approval_request = message
        
        reply = await verification_channel.send(embed=embed)
        embed = discord.Embed(title="Application",
                              description=f"**Username:** {message.content}", color=0x00ff00)
        embed.set_image(url=message.attachments[0].url)
        await approval_channel.send(embed=embed, view=VerificationView(self.bot, message.author.id, message.content, approval_request, reply))
        
def setup(bot):
    bot.add_cog(Verify(bot))
        
