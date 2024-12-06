import discord
from discord.ext import commands
import os
import motor
import motor.motor_asyncio
from Utils.modules import get_guild_configuration
from Utils.client import Cog
from Utils.emojis import Emojis
from Cogs.Config.views import SelectView

class ConfigCog(Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)  
        self.bot = bot
    
    @commands.hybrid_command(name=f"config", description=f"Configure the bot")
    async def config(self, ctx: commands.Context):
        emojis = Emojis()
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** you can't use this.")
        config = await get_guild_configuration(mongo_connection=self.bot.mongo, guild_id=ctx.guild.id)
        if isinstance(config, bool):
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** please try again.", ephemeral=True)
        msg = await ctx.send(content=f"{emojis.yes_emoji} **{ctx.author.name},** you are now configuring curly.")
        await msg.edit(view=SelectView(timeout=600, ctx=ctx, message=msg, mongo=self.bot.mongo))
            
        
        

        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(ConfigCog(client))    
