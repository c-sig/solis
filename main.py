import discord
import os

from discord import *

TOKEN = os.environ['SOLIS_TOKEN']
VERIFICATION = 1226182355908034630
APPROVAL = 1226182388531593267
ROLE_ID = 1226182521239244850
GUILD_ID = 1093029794406465596

intents = discord.Intents.all()
client = discord.Client(intents=intents)

class MyView(discord.ui.View):
    def __init__(self, user_id: int, message_content: str):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.message_content = message_content
    
    @discord.ui.button(label="Verify", row=0 ,style=discord.ButtonStyle.green)
    async def verify_callback(self, button, interaction):
        applicant = client.get_user(self.user_id)
        guild = client.get_guild(GUILD_ID)
        member = guild.get_member(self.user_id)
        
        role = guild.get_role(ROLE_ID)
        await member.add_roles(role)
        
        await member.edit(nick=self.message_content)
        
        await interaction.response.edit_message(view=None)
        
        embed = discord.Embed(title="Application approved!", description="Thank you for applying! Please get your roles in the server to get started! Bridgewatch on top!", color=0x00ff00)
        await applicant.send(embed=embed)
        
    @discord.ui.button(label="Reject", row=1, style=discord.ButtonStyle.red)
    async def reject_callback(self, button, interaction):
        applicant = client.get_user(self.user_id)
        await interaction.response.edit_message(view=None)
        embed = discord.Embed(title="Application rejected!", description="Reapply when you can. Please make sure you send your exact username and a screenshot of your faction screen with your username visible.", color=0xff0000)
        await applicant.send(embed=embed)
        

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
@client.event
async def on_message(message):
    verification_channel = client.get_channel(VERIFICATION)
    approval_channel = client.get_channel(APPROVAL)

    if message.author == client.user:
        return
    
    if message.channel.id != VERIFICATION:
        return
    
    if not message.attachments:
        embed = discord.Embed(title="Missing screenshot!", description="Please send your screenshot in the same message as your username!", color=0xff0000)
        reply = await verification_channel.send(embed=embed)        
        await message.delete(delay=1)
        await reply.delete(delay=5)
        return
    
    if not message.content:
        embed = discord.Embed(title="Missing username!", description="Please send your username in the same message as your screenshot!", color=0xff0000)
        reply = await verification_channel.send(embed=embed)
        await message.delete(delay=1)
        await reply.delete(delay=5)
        return
    
    embed = discord.Embed(title="Application submitted!", description="Thank you for applying! Please wait for staff to review your application.", color=0x00ff00)
    reply = await verification_channel.send(embed=embed)
    await message.delete(delay=1)
    await reply.delete(delay=5)
    embed = discord.Embed(title="Application", description=f'**Username:** {message.content}\n', color=0x00ff00)
    embed.set_image(url=message.attachments[0].url) 
    await approval_channel.send(embed=embed, view=MyView(user_id=message.author.id, message_content=message.content))

client.run(TOKEN)