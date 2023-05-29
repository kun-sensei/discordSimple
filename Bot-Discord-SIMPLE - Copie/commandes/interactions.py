import discord
from discord import ui
from discord.ui import Button, Item, Modal, Select, TextInput, View

from commandes.tools import *


# Form Pseudo
class FormPseudo(Modal, title="Pseudo"):
    pseudo = TextInput(label="Votre pseudo", style=discord.TextStyle.short, required=True, max_length=32)

    # Response Pseudo
    async def on_submit(self, interaction: discord.Interaction):
        
        pseudo = str(self.pseudo)

        data = await getData()
        data["service"]["tickets"][str(interaction.user.id)]["pseudo"] = pseudo
        await saveData(data)

        await interaction.response.send_message("Votre pseudo a bien été enregistré !", ephemeral=True)