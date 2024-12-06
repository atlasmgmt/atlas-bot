from discord.ext import commands
from discord import Color
import discord
from motor.motor_asyncio import AsyncIOMotorClient
import os
from Utils.modules import get_guild_configuration


class StaffTeamRole(discord.ui.RoleSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection
        super().__init__(placeholder="Select a staff role", max_values=3, min_values=1, row=1)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        role_ids = []
        for role in self.values: role_ids.append(role.id)
        config = await get_guild_configuration(mongo_connection=self.mongo, guild_id=interaction.guild.id)
        db = self.mongo["Curly"]["Config"]
        await db.update_one(config, {"$set": {"staff_roles": role_ids}})
        return


class ManagementRole(discord.ui.RoleSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection

        super().__init__(placeholder="Select a management role", max_values=3, min_values=1, row=2)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        role_ids = []
        for role in self.values: role_ids.append(role.id)
        config = await get_guild_configuration(mongo_connection=self.mongo, guild_id=interaction.guild.id)
        db = self.mongo["Curly"]["Config"]
        await db.update_one(config, {"$set": {"management_roles": role_ids}})
        return


class PermissionsView(discord.ui.View):
    def __init__(self, ctx,mongo_connection, message):
        super().__init__(timeout=None)
        self.message = message
        self.ctx = ctx
        self.mongo = mongo_connection
        self.staff_role_view = StaffTeamRole(ctx=self.ctx, mongo_connection=mongo_connection)
        self.management_role_view = ManagementRole(ctx=self.ctx, mongo_connection=mongo_connection)
        self.add_item(item=self.staff_role_view)
        self.add_item(item=self.management_role_view)
                
        from Cogs.Config.views import GlobalFinishedButton

            
        self.add_item(GlobalFinishedButton(message=self.message, ctx=self.ctx, mongo=self.mongo))