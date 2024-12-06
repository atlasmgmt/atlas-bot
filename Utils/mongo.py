import motor.motor_asyncio
import os
import uuid
import secrets
import hashlib
import time
from Utils.modules import get_guild_configuration

async def get_module_configuration(guild_id: int, module_name: str):
    """Gets the guild configuration for the module defined in module_name

    Args:
        guild_id (int): The Guild ID
        module_name (str): The name of the module and the object in the record

    Returns:
        list
    """
    try:
        mongo = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
        db = mongo["Curly"]["Config"]
        find = await get_guild_configuration(guild_id)
        if isinstance(find, bool):
            return False
        if find:
            data = find[module_name]
            if data:
                return data
        return False

    except:
        return False

async def create_module_configuration(guild_id: int, module_name: str):
    """Creates the guild configuration for the module defined in module_name

    Args:
        guild_id (int): The Guild ID
        module_name (str): The name of the module and the object in the record

    Returns:
        bool
    """
    try:
        mongo = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
        db = mongo["Curly"]["Config"]
        find = await get_guild_configuration(guild_id=guild_id, mongo_connection=mongo)
        if isinstance(find, bool):
            return False
        i = await db.update_one(find, {"$set": {f"{module_name}": {}}})
        return i

    except Exception as e:
        print(e)
        return False


def generate_advanced_unique_id():
    uuid_part = uuid.uuid4().hex
    
    random_part = secrets.token_hex(8)  
    
    time_part = str(int(time.time_ns()))[-8:] 
    
    raw_id = uuid_part + random_part + time_part
    unique_id = hashlib.sha256(raw_id.encode()).hexdigest()[:32]
    
    return unique_id