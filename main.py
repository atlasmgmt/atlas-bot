# Im Bored, Wise Words:
# An idiot admires complexity, a genius admires simplicity

import dotenv
dotenv.load_dotenv()
import sys
sys.dont_write_bytecode = True
import discord
from discord.ext import commands
import os
import asyncio
import dotenv
from cogwatch import watch
from Utils.mongo import generate_advanced_unique_id
from typing import Literal, Optional
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import jishaku
dotenv.load_dotenv()

TOKEN = os.getenv(os.getenv("env"))
intents = discord.Intents.all()


class bot(commands.AutoShardedBot):
    def __init__(self):
        self.mongo = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        super().__init__(command_prefix='!!', intents=intents)

    @watch(path='Cogs', preload=True)
    async def on_ready(self):
        await self.tree.sync()
        print('Bot ready.')
        await self.change_presence(activity=discord.CustomActivity(name=os.getenv("ACTIVITY")))
        
discordbot = bot()





           
    
if __name__ == '__main__':
    discordbot.run(token=TOKEN, reconnect=True)

    