import discord
import asyncio

from discord.ext import commands

GUILD_ID = 1093029794406465596

class PartyView(discord.ui.View):
    def __init__(self, bot, participants):
        super().__init__(timeout=None)
        self.bot = bot
        self.participants = participants
        self.choices = []
                  
        for member_id in self.participants:
            member_name = self.bot.get_user(member_id).name
            self.choices.append(discord.SelectOption(label=member_name,value=f"{member_id}"))
        
        select = discord.ui.Select(placeholder="Select an option", min_values=1, max_values=len(self.choices), options=self.choices)
        self.add_item(select)
        select.callback = self.select_callback

    async def select_callback(self, interaction: discord.Interaction):
        guild = self.bot.get_guild(GUILD_ID)
                
        await interaction.response.send_message(f"Selected: {interaction.data['values']}")
        
        for member_id in interaction.data['values']:
            member = guild.get_member(int(member_id))
            original_nick = member.nick
            await member.edit(nick=f"1 {member.nick}")
            await asyncio.sleep(7200)
            await member.edit(nick=f"{original_nick}")
        
            
class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command()
    async def check(self, ctx, channel: discord.VoiceChannel):
        vc = self.bot.get_channel(channel.id)
        member_ids = [member.id for member in vc.members]
        await ctx.respond("Choose flavor!", view=PartyView(bot=self.bot, participants=member_ids))
        
def setup(bot):
    bot.add_cog(Party(bot))