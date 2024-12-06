import discord 
from discord.ext import commands 
import Cogs.Config.Modules.pernissions
import Cogs.Config.Modules.verification
import Cogs.Config.Modules.welcome
from Utils.emojis import Emojis
import Cogs.Config.Modules
from Utils.mongo import get_module_configuration, create_module_configuration

emojis = Emojis()

class ModuleSelection(discord.ui.Select):
    def __init__(self, message, ctx, mongo):
        self.message = message
        self.mongo = mongo
        self.ctx = ctx
        options=[
            discord.SelectOption(label=f"Permissions", description=f"Configure the permissions module.", value=f"perms", emoji=emojis.permissions_emoji),
            discord.SelectOption(label=f"Welcome", description=f"Configure the welcome module.", value=f"welcome", emoji=emojis.welcome_emoji),
            discord.SelectOption(label=f"Verification", description=f"Configure the verification module.", value=f"verification", emoji=emojis.verification_emoji)
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.values[0] == "perms":
            return await self.message.edit(content=f"{emojis.info_emoji} **{interaction.user.name},** you are configuring the permission module.", view=Cogs.Config.Modules.pernissions.PermissionsView(ctx=self.ctx, mongo_connection=self.mongo, message=self.message))
        if self.values[0] == "welcome":
            create = await create_module_configuration(interaction.guild.id, "WelcomeModule")
            if create is False: 
                return await self.message.edit(content=f"{emojis.info_emoji} **{interaction.user.name},** please retry the command.")
            return await self.message.edit(content=f"{emojis.info_emoji} **{interaction.user.name},** you are configuring the welcome module.", view=Cogs.Config.Modules.welcome.WelcomeView(ctx=self.ctx, mongo_connection=self.mongo, message=self.message))
        
        if self.values[0] == "verification":
            create = await create_module_configuration(interaction.guild.id, "VerifyModule")
            if create is False: 
                return await self.message.edit(content=f"{emojis.info_emoji} **{interaction.user.name},** please retry the command.")
            return await self.message.edit(content=f"{emojis.info_emoji} **{interaction.user.name},** you are configuring the verification module.", view=Cogs.Config.Modules.verification.VerificationView(ctx=self.ctx, mongo_connection=self.mongo, message=self.message))
        

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, ctx, message, mongo):
        self.ctx= ctx
        self.message = message
        self.mongo = mongo
        super().__init__(timeout=timeout)
        self.add_item(ModuleSelection(ctx=self.ctx, message=self.message, mongo=self.mongo))
        
        

        

class GlobalFinishedButton(discord.ui.Button):
    def __init__(self, ctx, message, mongo):
        super().__init__(style=discord.ButtonStyle.gray, label="Done", row=4)
        self.ctx = ctx
        self.message = message
        self.mongo = mongo
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return

        await interaction.response.defer()

        await self.message.edit(content=f"{emojis.yes_emoji} **{interaction.user.display_name},** you are now configuring curly.", view=SelectView(ctx=self.ctx, message=self.message, mongo=self.mongo), embed=None)
            

        


        
        
