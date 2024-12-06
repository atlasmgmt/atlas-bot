from discord.ext import commands
import discord
from jishaku.features.baseclass import Feature
from jishaku.cog import OPTIONAL_FEATURES, STANDARD_FEATURES
import os
import motor.motor_asyncio

class CustomDebugCog(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    pass
async def setup(bot: commands.Bot):
    await bot.add_cog(CustomDebugCog(bot=bot))