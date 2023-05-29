import discord, os, time
from discord.ext import commands, tasks
from config import *
from commandes.tools import *

client = commands.Bot(command_prefix=PREFIX, help_command=None, intents=discord.Intents.all())

# Bot
@client.event
async def on_ready():
    for directory in os.listdir("commandes"):
        if os.path.isdir(f"commandes/{directory}"):
            for file in os.listdir(f"commandes/{directory}"):
                if file.endswith(".py"):
                    await client.load_extension(f"commandes.{directory}.{file[:-3]}")

    await client.tree.sync()

    print(f"\n{NAME} est prêt !\n")

# Reload
@client.command()
@commands.has_permissions(manage_messages=True)
async def reload(ctx, ext):
    await ctx.message.delete()
    await client.unload_extension(f"commandes.{ext}")
    await client.load_extension(f"commandes.{ext}")

    await ctx.send(f"**`{ext} rechargé !`**", delete_after=4)

@tasks.loop(seconds=10)
async def UpdateTime():
    data = await getData()
    villes = ["Draconiros", "Hellmina", "Tylezia", "Imagiro", "Orukam", "Talkasha"]

    for ville in villes:
        ville = f"ville{ville}"
        print(ville)

        if data["service"]["timestamps"][ville]["public"] != {}:

            for user_id in data["service"]["timestamps"][ville]["public"]:
                print(user_id)

                user = discord.utils.get(client.guilds[0].members, id=user_id)
                role_id = data["service"]["timestamps"][ville]["public"][user_id][0]
                role = discord.utils.get(client.guilds[0].roles, id=role_id)
                timeout = data["service"]["timestamps"][ville]["public"][user_id][1]

                if round(time.time()) >= timeout:

                    try:
                        user.remove_roles(role)
                        user.send(f"Le rôle {role.name} vous a été retiré car 1 semaine est passée.")

                    except Exception as e: print(e)


client.run(TOKEN)