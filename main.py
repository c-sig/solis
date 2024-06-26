import discord
import os

from discord import *

TOKEN = os.environ['SOLIS_TOKEN']

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

bot.load_extension('cogs.verify')
bot.load_extension('cogs.timer')
bot.load_extension('cogs.party')
bot.load_extension('cogs.signup')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)  