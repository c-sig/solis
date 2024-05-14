import discord
from discord.ext import commands

class SignUpView(discord.ui.View):
    def __init__(self, bot, roles, embed):
        super().__init__(timeout=None)
        self.bot = bot
        self.roles = roles
        self.embed = embed
        self.choices = []

        for role in self.roles:
            self.choices.append(discord.SelectOption(label=role, value=f"{role}"))

        select = discord.ui.Select(placeholder="Select an option", min_values=1, max_values=len(self.choices), options=self.choices)
        self.add_item(select)
        select.callback = self.select_callback

    async def select_callback(self, interaction: discord.Interaction):
        dict_embed = self.embed.to_dict()
        for field in dict_embed['fields']:
            for label in interaction.data['values']:
                label = label.strip()
                if field['name'] == label:
                    if interaction.user.nick in field["value"]:
                        # Remove the user's nick from the value
                        names = field["value"].split(", ")
                        names.remove(interaction.user.nick)
                        if names: # Check if there are any names left
                            field["value"] = ", ".join(names)
                        else: 
                            field["value"] = "Unassigned" # Reset to "Unassigned"
                    else:
                        # Add the user's nick to the value
                        if field["value"] == "Unassigned":
                            field["value"] = interaction.user.nick
                        else:
                            field["value"] = field["value"] + ", " + interaction.user.nick
                    break

        # Update the embed with the modified 'fields'
        self.embed = discord.Embed.from_dict(dict_embed) 
        await interaction.response.edit_message(embed=self.embed)

class SignUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Sign up for a role!")
    async def mass(self, ctx, roles: str, title: str):
        roles = roles.split(",")
        roles = [role.strip() for role in roles]  # Remove leading/trailing spaces
        embed = discord.Embed(title=title, color=0x00ff00, description="Select the role you want to play by using the dropdown below!")
        for role in roles:
            embed.add_field(name=role, value="Unassigned", inline=True)
        view = SignUpView(bot=self.bot, roles=roles, embed=embed)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(SignUp(bot))