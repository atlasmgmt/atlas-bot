import discord
from discord.ext import commands, tasks
import os
import motor
import motor.motor_asyncio
from Utils.mongo import get_module_configuration
from Utils.client import Cog
from Utils.emojis import Emojis
emojis=Emojis()
class CurlyCog(Cog):
    def __init__(self, client: commands.Bot):
        super().__init__(client)  
        self.bot = client    
        self.running = False
        
    @commands.Cog.listener(name="on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(color=discord.Color.from_str("#BAFF29"), title=guild.name, description=f"**Owner:** <@{guild.owner_id}> ({guild.owner_id})\n**Guild:** {guild.name} ({guild.id})\n**Members:** {guild.member_count}\n**Created On:** {discord.utils.format_dt(guild.created_at, "F")}")
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        channel = self.bot.get_channel()
    
    @commands.hybrid_group(name=f"premium", description=f"Premium based commands")     
    async def premium(self, ctx: commands.Context):
        pass
    
    @premium.command(name=f"add", description=f"Give a server premium")
    async def add_premium(self, ctx: commands.Context, guild_id: int):
        if ctx.author.id not in [856971748549197865, 527166312095678475, 937122696003747930]:
            return
        
    @commands.group(name=f"atlas")
    async def atlas(self, ctx):
        if ctx.author.id not in [856971748549197865, 527166312095678475, 937122696003747930]:
            return
    @atlas.command(name=f"infopanel")
    async def infopanel(self, ctx: commands.Context, channel: discord.TextChannel):
        if ctx.author.id not in [856971748549197865, 527166312095678475, 937122696003747930]:
            return    
        
        banner_embed = discord.Embed(title="", description="", color=discord.Color.from_str("#BAFF29"))
        banner_embed.set_image(url="https://cdn.imgchest.com/files/j7kzclqbr27.png")
        embed = discord.Embed(title="Atlas", description="", color=discord.Color.from_str("#BAFF29"))
        embed.add_field(name="What is Atlas?", value="Atlas is a discord bot based completely at making your roblox shop run better then ever before.", inline=True)
        embed.add_field(name="Why should I use Atlas?", value="Atlas strives to be better in nearly every aspect over our competition, we believe that bigger is not always better.", inline=True)
        embed.add_field(name="When was Atlas founded?", value="Atlas was founded on the **29th June 2024** and has continued to operate since.", inline=True)
        embed.set_image(url="https://cdn.imgchest.com/files/d7ogczokz5y.png")
        await channel.send(embeds=[banner_embed, embed])
        return await ctx.send(content=f"{emojis.yes_emoji} **{ctx.author.name},** I have sent the panel.")
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(CurlyCog(client))