from discord.ext import commands
from discord import Color
import discord
from motor.motor_asyncio import AsyncIOMotorClient
import os
from Utils.modules import get_guild_configuration
from Utils.mongo import get_module_configuration
import validators
from Utils.embeds import clean_input
from Utils.menus import CustomModal

class WelcomeEmbedCreation(discord.ui.View):
    def __init__(self, *, timeout=180, ctx, message, mongo):
        self.ctx = ctx
        self.message = message
        self.mongo = mongo
        self.msg_content = None
        self.embed=discord.Embed(color=discord.Color.dark_embed(), title="Set Title", description="Set Description")
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="Finished", style=discord.ButtonStyle.blurple)
    async def EmbedFinished(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        json = self.embed.to_dict()  
        module = await get_module_configuration(interaction.guild.id, "WelcomeModule")  
        db = self.mongo["Curly"]["Config"]

        if module is None:
            await interaction.response.send_message("The WelcomeModule configuration was not found.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        print(f"Updating WelcomeModule for guild_id: {guild_id} with content: {json}")

        result = await db.update_one(
            {"guild_id": guild_id},  
            {"$set": {"WelcomeModule.content": json, "WelcomeModule.msg_content": self.msg_content}} 
        )

        if result.modified_count > 0:
            await interaction.response.send_message("The welcome embed has been updated successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("No changes were made. Please check if the WelcomeModule exists.", ephemeral=True)
        

    @discord.ui.button(label="Title", style=discord.ButtonStyle.blurple)
    async def EmbedTitle(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Title", style=discord.TextStyle.short, custom_id="embed_title"))
        ]

        modal = CustomModal(title="Edit Embed Title", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        user_input = getattr(modal, "text_input", "No Title Provided")  
        self.embed.title = user_input
        await self.message.edit(embed=self.embed)
        
    
    @discord.ui.button(label="Content", style=discord.ButtonStyle.blurple)
    async def MessageContent(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Message Content", style=discord.TextStyle.short, custom_id="messagE_content"))
        ]

        modal = CustomModal(title="Edit Message Content", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        user_input = getattr(modal, "text_input", "No Message Provided")  
        await self.message.edit(content=user_input)
        
        
    @discord.ui.button(label="Description", style=discord.ButtonStyle.blurple)
    async def EmbedDescription(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Description", style=discord.TextStyle.short, custom_id="embed_description"))
        ]

        modal = CustomModal(title="Edit Embed Description", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        user_input = getattr(modal, "text_input", "No Description Provided")  
        self.embed.description = None
        self.embed.description = user_input
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Color", style=discord.ButtonStyle.blurple)
    async def EmbedColor(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Color", style=discord.TextStyle.short, custom_id="embed_color"))
        ]

        modal = CustomModal(title="Edit Embed Color", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Color Provided")  
        if "#" not in user_input:
            return await interaction.followup.send(content=f"**{interaction.user.name},** please provide a valid HEX code!", ephemeral=True)
        self.embed.color = None
        cleaned_string = user_input[1:]
        try:
            self.embed.color = discord.colour.parse_hex_number(cleaned_string)
        except Exception as e:
            print(e)
            return await interaction.followup.send(content=f"**{interaction.user.name},** please provide a valid HEX code!", ephemeral=True)
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Content", style=discord.ButtonStyle.gray)
    async def MessageContent(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f" **{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Message Content", style=discord.TextStyle.short, custom_id="message_content"))
        ]

        modal = CustomModal(title="Edit Message Content", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Content Provided")  
        await self.message.edit(content=user_input)
        
    @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.gray)
    async def EmbedThumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Thumbnail", style=discord.TextStyle.short, custom_id="embed_thumbnail"))
        ]

        modal = CustomModal(title="Edit Embed Thumbnail", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Thumbnail Provided")  
        validation = validators.url(user_input)
        if validation:
            self.embed.set_thumbnail(url=user_input)
        else:
            await interaction.followup.send(content=f"**{interaction.user.name},** that is not a valid URL!")
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Image", style=discord.ButtonStyle.gray)
    async def EmbedImage(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Thumbnail", style=discord.TextStyle.short, custom_id="embed_image"))
        ]

        modal = CustomModal(title="Edit Embed Image", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Image Provided")  
        validation = validators.url(user_input)
        if validation:
            self.embed.set_image(url=user_input)
        else:
            await interaction.followup.send(content=f"**{interaction.user.name},** that is not a valid URL!")
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Author", style=discord.ButtonStyle.gray)
    async def AuthorName(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return
        options = [
            ("text_input", discord.ui.TextInput(
                label="Embed Author Name",
                style=discord.TextStyle.short,
                custom_id="embed_author_name")),
            ("text_input2", discord.ui.TextInput(
                label="Embed Author Icon",
                style=discord.TextStyle.paragraph, 
                custom_id="embed_author_icon"  
                ))
            ]
        modal = CustomModal(title="Edit Embed Author", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Name Provided")  
        user_input2 = getattr(modal, "text_input2", "No Icon Provided")  
        validation = validators.url(user_input2)
        if validation:
            self.embed.set_author(name=user_input, icon_url=user_input2)
        else:
            await interaction.followup.send(content=f"**{interaction.user.name},** that is not a valid URL!")
        await self.message.edit(embed=self.embed)
        
            
    @discord.ui.button(label="Footer", style=discord.ButtonStyle.gray)
    async def FooterName(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return
        options = [
            ("text_input", discord.ui.TextInput(
                label="Embed Footer Name",
                style=discord.TextStyle.short,
                custom_id="embed_footer_name")),
            ("text_input2", discord.ui.TextInput(
                label="Embed Footer Icon",
                style=discord.TextStyle.paragraph, 
                custom_id="embed_footer_icon",
                required=False
                ))
            ]
        modal = CustomModal(title="Edit Embed Footer", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        user_input1 = clean_input(getattr(modal, "text_input", ""))
        user_input2 = clean_input(getattr(modal, "text_input2", ""))

        validation = validators.url(user_input2)
        if validation:
            self.embed.set_footer(text=user_input1, icon_url=user_input2)
        else:
            if user_input2 is None:
                self.embed.set_footer(text=user_input1)
            else: await interaction.followup.send(content=f"**{interaction.user.name},** that is not a valid URL!")
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.gray)
    async def AddField(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(
                label="Field Name",
                style=discord.TextStyle.short,
                custom_id="embed_add_field_name")),
            ("text_input2", discord.ui.TextInput(
                label="Field Value",
                style=discord.TextStyle.paragraph, 
                custom_id="embed_add_field_value",
                required=True
                )),
            
            ("text_input3", discord.ui.TextInput(
                label="Field Inline",
                style=discord.TextStyle.paragraph, 
                custom_id="embed_add_field_inline",
                required=True,
                placeholder="Yes or No"
                ))
            ]
        modal = CustomModal(title="Add Embed Field", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input1 = clean_input(getattr(modal, "text_input", ""))
        user_input2 = clean_input(getattr(modal, "text_input2", ""))
        user_input3 = clean_input(getattr(modal, "text_input3", ""))
        user_input3.lower()
        yes_values = ["Yes", "Sure", "yes", "sure", "true"]
        if user_input3 in yes_values:
            self.embed.add_field(name=user_input1, value=user_input2, inline=True)
        
        else:
            self.embed.add_field(name=user_input1, value=user_input2, inline=False)
            
        await self.message.edit(embed=self.embed)
        
    @discord.ui.button(label="Clear Fields", style=discord.ButtonStyle.gray)
    async def ClearFields(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"**{interaction.user.name},** you can't use this!", ephemeral=True)
            return
        
        self.embed.clear_fields()
        await self.message.edit(embed=self.embed)
        

class WelcomeRole(discord.ui.RoleSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection
        super().__init__(placeholder="Select a welcome role", max_values=1, min_values=1, row=1)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        role_id = self.values[0].id
        db = self.mongo["Curly"]["Config"]
        await db.update_one({"guild_id": interaction.guild.id}, {"$set": {"WelcomeModule.role_id": role_id}})
        return


class WelcomeChannel(discord.ui.ChannelSelect):
    def __init__(self, mongo_connection, ctx):
        self.ctx = ctx
        self.mongo = mongo_connection

        super().__init__(placeholder="Select a welcome channel", max_values=1, min_values=1, row=2)

    async def callback(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        channel_id = self.values[0].id
        db = self.mongo["Curly"]["Config"]
        await db.update_one({"guild_id": interaction.guild.id}, {"$set": {"WelcomeModule.channel_id": channel_id}})
        return
    
class EmbedCreation(discord.ui.Button):
    def __init__(self, ctx, mongo):
        self.ctx = ctx
        self.mongo = mongo
        super().__init__(label=f"Change Embed", style=discord.ButtonStyle.gray)

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id == self.ctx.author.id:
            embed = discord.Embed(description="This is not your panel!", color=discord.Color.dark_embed())
            embed.set_author(icon_url=interaction.user.display_avatar.url)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()
        embed_message = discord.Embed(color=discord.Color.dark_embed(), title="Set Title", description="Set Description")
        
        message = await interaction.followup.send(embed=embed_message, ephemeral=True)
        
        await message.edit(view=WelcomeEmbedCreation(timeout=None, ctx=self.ctx, message=message, mongo=self.mongo))
            

class WelcomeView(discord.ui.View):
    def __init__(self, ctx,mongo_connection, message):
        super().__init__(timeout=None)
        self.message = message
        self.ctx = ctx
        self.mongo = mongo_connection
        self.welcome_role_view = WelcomeRole(ctx=self.ctx, mongo_connection=mongo_connection)
        self.welcome_channel_view = WelcomeChannel(ctx=self.ctx, mongo_connection=mongo_connection)
        self.embed_creation_view = EmbedCreation(ctx=self.ctx, mongo=mongo_connection)
        self.add_item(item=self.welcome_role_view)
        self.add_item(item=self.welcome_channel_view)
        self.add_item(item=self.embed_creation_view) 
        from Cogs.Config.views import GlobalFinishedButton

        
        self.add_item(GlobalFinishedButton(message=self.message, ctx=self.ctx, mongo=self.mongo))