import discord
from discord.ext import commands
import time
import traceback
from random import randint
import random
import roblox

from Utils.emojis import Emojis
emojis = Emojis()

from roblox import Client
import motor.motor_asyncio

from Utils.client import Cog
import string
import aiohttp
import json
from Utils.menus import YesNoMenuNoParams
from Utils.mongo import get_module_configuration
rclient = Client()

class VerifyHere(discord.ui.View):
    def __init__(self, mongo):
        super().__init__(timeout=None)
        self.mongo = mongo
        self.collection = mongo["Curly"]["Accounts"]
        
        


    @discord.ui.button(label="Verify Account", style=discord.ButtonStyle.green, custom_id=f"persistent_view:verify")
    async def done(self, interaction: discord.Interaction, button: discord.Button):
        try:

            find = await self.collection.find_one({"discord_id": interaction.user.id})
            if find:
                user = await rclient.get_user(find.get("roblox_id"))
                embed = discord.Embed(title=f"Account Found!", description=f"> A previous record for your account has been found, would you like to verify as **{user.name}?**", color=discord.Color.dark_embed())
                async with  aiohttp.ClientSession() as session:
                    async with session.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user.id},0&size=100x100&format=Png&isCircular=true") as resp:
                        if resp.status == 200:
                            data = json.loads(await resp.text())
                            image_url = data['data'][0]['imageUrl']

                        embed.set_thumbnail(url=image_url)
                        embed.set_author(icon_url=image_url, name=f"{user.name} ({user.id})")
                view = YesNoMenuNoParams(defer=True)
                await interaction.response.send_message(ephemeral=True, embed=embed, view=view)
                await view.wait()
                if view.value is True:
                    db = self.mongo["Curly"]["Config"]
                    config = await db.find_one({"guild_id": interaction.guild.id})["VerifyModule"]                    
                    try:
                        embed = discord.Embed(title=f"Verification Completed", description=f"{interaction.user.mention} has verified as ``{user.name}``.", color=discord.Color.green())
                        log_channel = interaction.guild.get_channel(config["log_channeL_id"])
                        await log_channel.send(embed=embed)
                    except KeyError:
                        pass                    
                    try:
                        verified_role = interaction.guild.get_role(config["verified_role_id"])
                    except KeyError:
                        verified_role = 0
                    try:
                        unverified_role = interaction.guild.get_role(config["unverified_role_id"])
                    except KeyError:
                        unverified_role = 0
                    
                    
                    if unverified_role != 0: 
                        await interaction.user.remove_roles(unverified_role)
                    if verified_role != 0:
                        await interaction.user.add_roles(verified_role)
                        await interaction.user.nick == f"{interaction.user.display_name} ({user.name})"
                    return await interaction.edit_original_response(content=f"**{interaction.user.name},** your verification has been completed.")
                
                if view.value is False:
                    await self.collection.delete_one({"discord_id": interaction.user.id, "roblox_id": user.id})
                    return await interaction.edit_original_response(content=f"**{interaction.user.name},** please click the verification panel again.")
            
            if not find:
                await interaction.response.send_modal(Username(interaction, self.mongo))
        except Exception as e:
            return await interaction.response.send_message(content=e, ephemeral=True)
            

class Done(discord.ui.View):
    def __init__(self, code, user, interaction, mongo):
        super().__init__()
        self.value = None
        self.user = user
        self.code = code
        self.mongo = mongo
        self.interaction = interaction
        self.collection = mongo["Curly"]["Accounts"]
        


    @discord.ui.button(label="Finished", style=discord.ButtonStyle.gray)
    async def done(self, interaction: discord.Interaction, button: discord.Button):
        user = await rclient.get_user_by_username(self.user, expand=True)
        description = user.description

        if self.code in description:
            find = await self.collection.find_one({"discord_id": interaction.user.id})
            if find:
                await self.collection.update_one({"discord_id": interaction.user.id},{"$set": {"roblox_id": user.id}})
            else:
                await self.collection.insert_one({"discord_id": interaction.user.id, "roblox_id": user.id})

            await interaction.response.defer()

            await self.interaction.edit_original_response(
                content=f"**{interaction.user.display_name},** I have succesfully linked this account to ``{user.name}``.",
                embed=None,
                view=None
            )
            db = self.mongo["Curly"]["Config"]
            config = await db.find_one({"guild_id": interaction.guild.id})["VerifyModule"]
            try:
                embed = discord.Embed(title=f"Verification Completed", description=f"{interaction.user.mention} has verified as ``{user.name}``.", color=discord.Color.green())
                log_channel = interaction.guild.get_channel(config["log_channeL_id"])
                await log_channel.send(embed=embed)
            except KeyError:
                pass                    
            try:
                verified_role = interaction.guild.get_role(config["verified_role_id"])
            except KeyError:
                verified_role = 0
            try:
                unverified_role = interaction.guild.get_role(config["unverified_role_id"])
            except KeyError:
                unverified_role = 0
                    
                    
            if unverified_role != 0: 
                await interaction.user.remove_roles(unverified_role)
            if verified_role != 0:
                await interaction.user.add_roles(verified_role)
                await interaction.user.nick == f"{interaction.user.display_name} ({user.name})"

        if self.code not in description:
            await self.interaction.edit_original_response(
                content=f"**{interaction.user.name},** I could not find ``{self.code}`` in your description. Please run the command again if you believe this is a mistake.",
                view=None,
                embed=None
            )
            
            
        

class Username(discord.ui.Modal):

    def __init__(self, ctx, mongo):
        

        self.collection = mongo["Curly"]["Accounts"]
        self.ctx=ctx
        self.mongo = mongo
        


        super().__init__(title="Roblox Verification")
        
        self.name = discord.ui.TextInput(
            label='Roblox Username',
            placeholder='What is your roblox username?',
            style=discord.TextStyle.short,
            required=True
        )
        
        self.add_item(self.name)
        

        

        



    async def on_submit(self, interaction: discord.Interaction):
        if self.ctx.user.id != interaction.user.id:
            return await interaction.response.send_message(f"**{interaction.user.display_name},** this is not your view!", ephemeral=True)
        user = await rclient.get_user_by_username(self.name.value, expand=True)
        options = ["car", "dog", "space", "school", "house", "cat", "person", "universe", "clothing", "game"]

        random_options = random.sample(options, 5)

        random_string = ", ".join(random_options)
        view = Done(code=random_string, user=user.name, interaction=interaction, mongo=self.mongo)
        embed = discord.Embed(color=discord.Color.dark_embed(), description=f"Hello **{interaction.user.name},** to verify ownership of the account ``{self.name.value}``, please put the provided code in the description of your roblox account, after that click the **Done** button\n\n **Account Information**\n> **Username:** ``{self.name.value}``\n> **User ID:** ``{user.id}``\n> **Profile Link:** https://roblox.com/users/{user.id}/profile\n\n**Enter This Code:**\n```{random_string}```")

        async with  aiohttp.ClientSession() as session:
            async with session.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user.id},0&size=100x100&format=Png&isCircular=true") as resp:
                if resp.status == 200:
                    data = json.loads(await resp.text())
                    image_url = data['data'][0]['imageUrl']

                    embed.set_thumbnail(url=image_url)
        await interaction.response.send_message(ephemeral=True, view=view, embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


    
class VerificationCog(Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)  
        self.bot = bot        
    @commands.hybrid_group(name=f"verification", description=f"Verification based commands")
    async def verification(self, ctx):
        pass
    
    @verification.command(name=f"panel", description=f"Send the verification panel.")
    async def verification_panel(self, ctx: commands.Context):
        db = self.bot.mongo["Curly"]["Config"]
        
        find = await db.find_one({"guild_id": ctx.guild.id})
        print(find)
        config = find["VerifyModule"]
        if not find: return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** please setup staff and management roles.", ephemeral=True)
        try:
            management_roles = find["management_roles"]
        except KeyError:
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** please setup the management roles.", ephemeral=True)
        user_roles = []
        for role in ctx.author.roles: user_roles.append(role.id)
        if not any(role in user_roles for role in management_roles):        
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** you need a management role to use this.", ephemeral=True)
        has_premium = False
        
        panel_channel = await ctx.guild.fetch_channel(config["panel_channel_id"])

        
        try:
            premium = find["premium"]
            if premium is True:
                has_premium = True
            else:
                has_premium = False
        except KeyError:
            has_premium = False
        
        if has_premium is True:
            try:
                content = find["VerifyModule.content"]
                embed = discord.Embed.from_dict(content)
                return await panel_channel.send(view=VerifyHere(mongo=self.bot.mongo), embed=embed)
            except:
                return await panel_channel.send(view=VerifyHere(mongo=self.bot.mongo), content=f"Gain access to **{ctx.guild.name}** by clicking the below button.")
        else:
            return await panel_channel.send(view=VerifyHere(mongo=self.bot.mongo), content=f"Gain access to **{ctx.guild.name}** by clicking the below button.")
    
            

async def setup(client: commands.Bot) -> None:
    await client.add_cog(VerificationCog(client))