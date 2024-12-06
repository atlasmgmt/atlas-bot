import json, discord
from Utils.menus import CustomModal
from Utils.mongo import create_module_configuration
import validators
import Utils.emojis
Emojis = Utils.emojis.Emojis()

def recursively_replace(obj, key, value):
    if isinstance(obj, str):
        return obj.replace(key, value)
    elif isinstance(obj, list):
        return [recursively_replace(item, key, value) for item in obj]
    elif isinstance(obj, dict):
        return {k: recursively_replace(v, key, value) for k, v in obj.items()}
    else:
        return obj
    
def clean_input(input_value):
    """
    Strips whitespace from the input value and returns None if it's empty.
    """
    stripped_value = input_value.strip() if input_value else ""
    return None if not stripped_value else stripped_value


class VerificationEmbedCreation(discord.ui.View):
    def __init__(self, *, timeout=180, ctx, message, mongo, module: str):
        self.ctx = ctx
        self.module = module
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
        module = await create_module_configuration(interaction.guild.id, self.module)  
        db = self.mongo["Curly"]["Config"]

        guild_id = interaction.guild.id
        result = await db.update_one(
            {"guild_id": interaction.guild.id},
            {
                "$setOnInsert": {self.module: {}},  
                "$set": {f"{self.module}.content": json, f"{self.module}.msg_content": self.msg_content},
            },
            upsert=True
        )        


        if result.modified_count > 0:
            await interaction.response.send_message(f"{Emojis.yes_emoji} **{interaction.user.name},** I have changed the embed.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** something went wrong.", ephemeral=True)
        

    @discord.ui.button(label="Title", style=discord.ButtonStyle.blurple)
    async def EmbedTitle(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Title.", ephemeral=True)
    
    @discord.ui.button(label="Message Content", style=discord.ButtonStyle.blurple)
    async def MessageContent(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Message Content", style=discord.TextStyle.short, custom_id="message_content"))
        ]

        modal = CustomModal(title="Edit Message Content", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        user_input = getattr(modal, "text_input", "No Message Provided")  
        await self.message.edit(content=user_input)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Content.", ephemeral=True)

        
        
    @discord.ui.button(label="Description", style=discord.ButtonStyle.blurple)
    async def EmbedDescription(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Description.", ephemeral=True)

        
    @discord.ui.button(label="Color", style=discord.ButtonStyle.blurple)
    async def EmbedColor(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
            return

        options = [
            ("text_input", discord.ui.TextInput(label="Embed Color", style=discord.TextStyle.short, custom_id="embed_color"))
        ]

        modal = CustomModal(title="Edit Embed Color", options=options)
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        
        user_input = getattr(modal, "text_input", "No Color Provided")  
        if "#" not in user_input:
            return await interaction.followup.send(content=f"{Emojis.no_emoji} **{interaction.user.name},** please provide a valid HEX code!", ephemeral=True)
        self.embed.color = None
        cleaned_string = user_input[1:]
        try:
            self.embed.color = discord.colour.parse_hex_number(cleaned_string)
        except Exception as e:
            print(e)
            await interaction.followup.send(f"{Emojis.no_emoji} **{interaction.user.name},** that is not a HEX code!", ephemeral=True)
        await self.message.edit(embed=self.embed)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Color.", ephemeral=True)


        
    @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.gray)
    async def EmbedThumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** that is not a URL!", ephemeral=True)
        await self.message.edit(embed=self.embed)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Thumbnail.", ephemeral=True)

        
    @discord.ui.button(label="Image", style=discord.ButtonStyle.gray)
    async def EmbedImage(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** that is not a URL!", ephemeral=True)
        await self.message.edit(embed=self.embed)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Image.", ephemeral=True)

        
    @discord.ui.button(label="Author", style=discord.ButtonStyle.gray)
    async def AuthorName(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** that is not a URL!", ephemeral=True)
        await self.message.edit(embed=self.embed)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Author.", ephemeral=True)

        
            
    @discord.ui.button(label="Footer", style=discord.ButtonStyle.gray)
    async def FooterName(self, interaction: discord.Interaction, button: discord.ui.Button):
        from validators.domain import domain
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have updated the Footer.", ephemeral=True)

        
    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.gray)
    async def AddField(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
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
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have added the field.", ephemeral=True)

        
    @discord.ui.button(label="Clear Fields", style=discord.ButtonStyle.gray)
    async def ClearFields(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"{Emojis.no_emoji} **{interaction.user.name},** you can't use this!", ephemeral=True)
            return
        
        self.embed.clear_fields()
        await self.message.edit(embed=self.embed)
        return await interaction.followup.send(f"{Emojis.yes_emoji} **{interaction.user.name},** I have cleared the fields.", ephemeral=True)