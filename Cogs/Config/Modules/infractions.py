from discord.ext import commands
from discord import Color
import discord
from motor.motor_asyncio import AsyncIOMotorClient
import os
from Utils.modules import get_guild_configuration
from Utils.emojis import Emojis
emojis=Emojis()


class InfractionChannel(discord.ui.ChannelSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection
        super().__init__(placeholder="Select a infraction channel", max_values=1, min_values=1, row=1)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        config = await get_guild_configuration(mongo_connection=self.mongo, guild_id=interaction.guild.id)
        db = self.mongo["Curly"]["Config"]
        result = await db.update_one(
            {"guild_id": interaction.guild.id},
            {
                "$setOnInsert": {"InfractionModule": {}},  
                "$set": {"InfractionModule.log_channel": self.values[0].id},
            },
            upsert=True
        )        
        return
    
class AppealsEnabledDisabled(discord.ui.Select):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection
        options = [
            discord.SelectOption(label='Enable Appeals', description='This will allow infracted users to appeal their infraction', value=True),
            discord.SelectOption(label='Disable Appeals', description='This will not allow infracted users to appeal their infraction', value=False),
        ]

        super().__init__(placeholder='Infraction Appeals', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        db = self.mongo["Curly"]["Config"]
        result = await db.update_one(
            {"guild_id": interaction.guild.id},
            {
                "$setOnInsert": {"InfractionModule": {}},  
                "$set": {"InfractionModule.appeals_enabled": self.values[0]},
            },
            upsert=True
        )  
        return await interaction.response.send_message(content=f"{emojis.yes_emoji} **{interaction.user.name},** infraction appeals are now {"enabled" if self.values[0] is True else "disabled"}")

    
class InfractionAppealChannel(discord.ui.ChannelSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection
        super().__init__(placeholder="Select a infraction appeal channel", max_values=1, min_values=1, row=1)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        config = await get_guild_configuration(mongo_connection=self.mongo, guild_id=interaction.guild.id)
        db = self.mongo["Curly"]["Config"]
        result = await db.update_one(
            {"guild_id": interaction.guild.id},
            {
                "$setOnInsert": {"InfractionModule": {}},  
                "$set": {"InfractionModule.appeal_channeL_id": self.values[0].id},
            },
            upsert=True
        )        
        return




class PermissionsView(discord.ui.View):
    def __init__(self, ctx,mongo_connection, message):
        super().__init__(timeout=None)
        self.message = message
        self.ctx = ctx
        self.mongo = mongo_connection
        self.infraction_channel = InfractionChannel(ctx=self.ctx, mongo_connection=mongo_connection)
        self.infraction_appeal_channel = InfractionAppealChannel(ctx=self.ctx, mongo_connection=mongo_connection)
        self.enabled_disabled = AppealsEnabledDisabled(ctx=self.ctx, mongo_connection=mongo_connection)
        self.add_item(item=self.infraction_channel)
        self.add_item(item=self.infraction_appeal_channel)
        self.add_item(item=self.enabled_disabled)
                
        from Cogs.Config.views import GlobalFinishedButton

            
        self.add_item(GlobalFinishedButton(message=self.message, ctx=self.ctx, mongo=self.mongo))