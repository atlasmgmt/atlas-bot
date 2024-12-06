import discord
from discord.ext import commands
import os
import motor
import motor.motor_asyncio
from Utils.client import Cog
from fastapi import APIRouter, Request, FastAPI
from uvicorn import Config,Server
from starlette.responses import JSONResponse
import asyncio
from Utils.client import Cog
import logging
import uvicorn
logging.basicConfig()
class API(Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)  
        self.bot = bot
    
    @commands.command(name=f"fastapi")
    async def fastapi(self, ctx: commands.Context):
        if ctx.author.id != 856971748549197865:
            return
        api = FastAPI()

        
        dashboard_router = APIRouter(tags=["Dashboard"])
        @dashboard_router.post(path="/guild/shared")
        async def shared_guilds(request: Request):
            try:
                body = await request.body()
                logging.debug(f"Raw Request Body: {body}")
                data = await request.json()
            except Exception as e:
                logging.error(f"Error parsing request body: {e}")
                return JSONResponse(content={"error": "Invalid JSON body"}, status_code=400)

            servers = data.get("servers", [])
            user_id = int(data.get("user_id"))
            mutual = []

            for server_id in servers:
                try:
                    guild = self.bot.get_guild(int(server_id)) 
                    member = guild.get_member(user_id)
                    if guild:
                        if member:
                            if member.guild_permissions.manage_guild:
                                mutual.append({
                                    "id": guild.id,
                                    "name": guild.name,
                                    "avatar": guild.icon.url if guild.icon else None,
                                    "members": guild.member_count,
                                })
                except Exception as e:
                    logging.error(f"Error processing guild {server_id}: {e}")

            return JSONResponse(content={"mutual_guilds": mutual}, status_code=200)
        
        @dashboard_router.post(path="/guild/allowed")
        async def guild_allowed(request: Request):
            data = await request.json()
            server_id = data.get("server_id", 0)
            user_id = data.get("user_id", 0)
            try:
                guild = self.bot.get_guild(int(server_id))
                if guild:
                    member = guild.get_member(int(user_id))
                    if member:
                        if member.guild_permissions.manage_guild:
                            return JSONResponse(content={"allowed": True}, status_code=200)
            except:
                return JSONResponse(status_code=200)
                        
                
    
        api.include_router(router=dashboard_router, prefix="/dashboard", tags=["Dashboard"])
        config = Config(
            app=api,
            host="127.0.0.1",#"0.0.0.0" if os.getenv("env") == "prod" else "127.0.0.1",
            port=5050)
        server = Server(config)    
        loop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(server.serve(), loop)
            


async def setup(client: commands.Bot) -> None:
    await client.add_cog(API(client))
    