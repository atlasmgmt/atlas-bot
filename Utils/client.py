from main import bot
from discord.ext import commands
from fastapi import FastAPI
import os
class Cog(commands.Cog): 
    def __init__(self, bot: bot):
        self.bot = bot
        self.fastapi = FastAPI()
        
        