import motor.motor_asyncio
import os
async def get_guild_configuration(mongo_connection, guild_id):
    """Create a basic guild configuration within the database

    Args:
        guild_id (int): The Guild ID

    Returns:
        list: If either a record has been created or a record has been found
        bool: If the function failed to find or create a record
    """
    try:
        db = mongo_connection["Curly"]["Config"]
        find = await db.find_one({"guild_id": guild_id})
        if find:
            return find
        insert = await db.insert_one({"guild_id": guild_id})
        if insert:
            return insert
        return False
    except Exception:
        return False

    