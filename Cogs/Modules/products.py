import discord
from discord.ext import commands
import os
import motor
import motor.motor_asyncio
from Utils.mongo import get_module_configuration, generate_advanced_unique_id
from Utils.client import Cog
from ro_py import Client
from Utils.emojis import Emojis
from Utils.menus import YesNoMenu
import io  # For handling byte streams

emojis = Emojis()

class ProductCog(Cog):
    def __init__(self, client: commands.Bot):
        super().__init__(client)  
        self.bot = client    
        self.mongo_uri = os.getenv("MONGO_URI")
        
    @commands.hybrid_group(name="product", description="Product based commands")
    async def product(self, ctx):
        pass
    
    @product.command(name="create", description="Make a brand new product")
    async def make_product(self, ctx: commands.Context, roblox_shirt_id: int, source_file: discord.Attachment, quantity: int):
        db = self.bot.mongo["Curly"]["Products"]
        find = await db.find_one({"guild_id": ctx.guild.id})
        print(find)
        config = find["VerifyModule"]
        if not find: 
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** please setup staff and management roles.", ephemeral=True)
        try:
            management_roles = find["management_roles"]
        except KeyError:
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** please setup the management roles.", ephemeral=True)
        
        user_roles = [role.id for role in ctx.author.roles]
        if not any(role in user_roles for role in management_roles):        
            return await ctx.send(content=f"{emojis.no_emoji} **{ctx.author.name},** you need a management role to use this.", ephemeral=True)
        
        client = Client()
        try:
            item = await client.get_asset(roblox_shirt_id)
            if item:
                product_id = generate_advanced_unique_id()
                file_bytes = await source_file.read()
                view = YesNoMenu(user_id=ctx.author.id)
                embed = discord.Embed(color=discord.Color.orange(), title=f"Please confirm the product.", description=f"**Asset:** {item.name} ({item.id})\n**Price:** {item.price}$R\n**Quantity:** {quantity}")
                embed.set_footer(text=f"Product ID: {product_id}")
                msg = await ctx.send(embed=embed, ephemeral=True, view=view)
                await view.wait()
                if view.value is False:
                    return await msg.edit(content=f"{emojis.no_emoji} **{ctx.author.name},** please re run the command.", ephemeral=True)
                await db.insert_one({
                    "guild_id": ctx.guild.id,
                    "product_id": product_id,
                    "item_id": item.id,
                    "item_name": item.name,
                    "price": item.price,
                    "quantity": quantity,
                    "source_file": file_bytes  
                })
                return await msg.edit(f"{emojis.yes_emoji} **{ctx.author.name},** the product has been successfully added.")
                
        except Exception as e:
            return await ctx.send(e)
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(ProductCog(client))
