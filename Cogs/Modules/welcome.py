import discord
from discord.ext import commands
import os
import motor
import motor.motor_asyncio
from Utils.mongo import get_module_configuration
from Utils.client import Cog
class WelcomeCog(Cog):
    def __init__(self, client: commands.Bot):
        super().__init__(client)  
        self.bot = client    
        self.mongo_uri = os.getenv("MONGO_URI")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        data = await get_module_configuration(guild_id=member.guild.id, module_name="WelcomeModule")
        if isinstance(data, bool):
            return

        try:
            channel_id = data["channel_id"]
            role_id = data["role_id"]
            content = data["content"]
            msg_content = data["msg_content"]
        except KeyError:
            return


        replacements = {
            "{user.name}": member.name,
            "{user.mention}": member.mention,
            "{guild.member_count}": str(member.guild.member_count), 
            "{user.avatar_url}": member.display_avatar.url,
            "{user.id}": str(member.id), 
            "{guild.name}": member.guild.name,
            "{guild.icon_url}": member.guild.icon.url if member.guild.icon else ""
        }

        embed_dict = self.replace_placeholders(content, replacements)
        msg = self.replace_placeholders(msg_content, replacements)
        embed = discord.Embed().from_dict(embed_dict)

        channel = await member.guild.fetch_channel(channel_id)
        await channel.send(embed=embed, content=msg)

        if role_id is not None:
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)

    def replace_placeholders(self, obj, replacements):
        """
        Recursively replace placeholders in the embed content using the replacements dictionary.
        """
        if isinstance(obj, str):
            for key, value in replacements.items():
                obj = obj.replace(key, str(value)) 
            return obj
        elif isinstance(obj, list):
            return [self.replace_placeholders(item, replacements) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.replace_placeholders(v, replacements) for k, v in obj.items()}
        else:
            return obj

async def setup(client: commands.Bot) -> None:
    await client.add_cog(WelcomeCog(client))