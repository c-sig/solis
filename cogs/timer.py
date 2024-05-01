import datetime
from discord.ext import commands
from discord.ext import tasks

TIME_CHANNEL = 1231627268095479978

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.update_time.start()
    
    @tasks.loop(minutes=10)
    async def update_time(self):
        channel = self.bot.get_channel(TIME_CHANNEL)
        await channel.edit(name="UTC: " + str(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")))
        
def setup(bot):
    bot.add_cog(Timer(bot))
    