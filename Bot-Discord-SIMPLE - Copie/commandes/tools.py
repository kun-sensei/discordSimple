import discord, asyncio, json
from config import *

# Récupération
async def getData(f="tickets", encoding="utf-8"):
    with open(f"./database/{f}.json", "r", encoding=encoding) as file: data = json.load(file)
    return data

# Sauvegarde
async def saveData(data, f="tickets", encoding="utf-8"):
    with open(f"./database/{f}.json", "w", encoding=encoding) as file: json.dump(data, file, indent=4)

# tasks.py
async def refresh_interactions(bot):
    for guild in bot.guilds:
        try:
            await bot.http.request(
                discord.http.Route("PATCH", f"/guilds/{guild.id}/commands"), 
                json=bot.application_command_guild_ids,
            )
        except discord.HTTPException as e:
            print(f"Impossible de mettre à jour les interactions dans la guilde {guild.name}: {e}")
