import discord, os, time
from discord.ext import commands

from commandes.tools import *
from config import *
from commandes.interactions import *


class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
    # ticket
    @commands.command()
    async def ticket(self, ctx):
        await ctx.message.delete()

        support_channel_id = 1103412714887463013 # Channel du panel
        
        support_channel = self.client.get_channel(support_channel_id)
        EmbedTicket = discord.Embed( description="Veuillez sélectionner la raison de votre ticket en appuyant sur un bouton ci-dessous. (Si le ticket ne fonctionne plus, contactez Sensei Kun directement par MP)", color=COLOR)
        # Boutons de l'embed TICKET
        class View_Ticket(discord.ui.View):
            # Bouton SERVICE
            @discord.ui.button(style=discord.ButtonStyle.gray, label=" 🛎️ SERVICE")
            async def button_service(self, interaction: discord.Interaction, button_service: discord.ui.button):
                data = await getData()
                tickets_nb = data["service"]["tickets_nb"]["total"]
                tickets_nb += 1

                transcript_channel_id = 1103402319200137217 # Salon des logs
                ticket_role_id = 999539733459914844 # Rôle ayant les permissions de voir les tickets
                open_cat_id = 902038839860805675 # Catégorie des tickets ouverts

                transcript_channel = interaction.client.get_channel(transcript_channel_id)
                ticket_role = interaction.guild.get_role(int(ticket_role_id))
                open_cat = await interaction.client.fetch_channel(str(open_cat_id))
                ticket_channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-{tickets_nb}", category=open_cat)

                await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False, read_messages=False)
                await ticket_channel.set_permissions(interaction.user, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                await ticket_channel.set_permissions(ticket_role, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                await ticket_channel.send(f"{interaction.user.mention} {ticket_role.mention}")

                EmbedTicketServiceWelcome = discord.Embed(title="Bienvenue !", description="Veuillez suivre les étapes demandées ci-dessous.", color=COLOR)
                EmbedTicketServiceLogs = discord.Embed(title=f"Ticket Service - {interaction.user.name}", description=f"{interaction.user.mention} a ouvert un ticket service.\n\n*Ticket : {ticket_channel.mention}*", color=0x32a852)

                await transcript_channel.send(embed=EmbedTicketServiceLogs)

                EmbedTicketServiceMessage = discord.Embed(title="Ticket - Service", description=f"Vous venez de créer un ticket service.\nVotre ticket : {ticket_channel.mention}", color=COLOR)
                await interaction.response.send_message(embed=EmbedTicketServiceMessage, ephemeral=True)


                # Boutons de l'embed TICKETSERVICEWELCOME
                class View_TicketServiceWelcome(discord.ui.View):

                    # Bouton FERMER
                    @discord.ui.button(style=discord.ButtonStyle.red, label="Fermer")
                    async def button_closeask(self, interaction: discord.Interaction, button_closeask: discord.ui.button):

                        EmbedTicketServiceCloseAsk = discord.Embed(title="Ticket Service - Fermeture", description="Êtes-vous sûr de vouloir fermer le ticket ?", color=COLOR)

                        class View_TicketServiceCloseAsk(discord.ui.View):

                            @discord.ui.button(style=discord.ButtonStyle.red, label="Non")
                            async def button_closecancel(self, interaction: discord.Interaction, button_closecancel: discord.ui.button):

                                await interaction.message.delete()

                            @discord.ui.button(style=discord.ButtonStyle.green, label="Oui")
                            async def button_close(self, interaction: discord.Interaction, button_close: discord.ui.button):

                                await interaction.message.delete()

                                data = await getData()

                                close_cat_id = 986436971461242890 # Catégorie des tickets fermés
                                transcript_channel_id = 1103402319200137217 # Channel des logs
                                close_cat = await interaction.client.fetch_channel(str(close_cat_id))
                                transcript_channel = interaction.client.get_channel(transcript_channel_id)

                                for ticket_id, ticket_user_id, msg_id in data["service"]["tickets"]["open"]:
                                    if ticket_id == interaction.channel.id:
                                        ticket_user = interaction.client.get_user(ticket_user_id)
                                        msg = await interaction.channel.fetch_message(msg_id)
                                        break

                                await msg.delete()

                                await interaction.channel.set_permissions(ticket_user, view_channel=False, read_messages=False, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False)

                                index = data["service"]["tickets"]["open"].index(list([interaction.channel.id, ticket_user_id, msg_id]))

                                del data["service"]["tickets"]["open"][index]
                                data["service"]["tickets"]["close"].append(tuple([interaction.channel.id, ticket_user_id, msg_id]))

                                await interaction.channel.edit(category=close_cat)

                                EmbedTicketServiceCloseLogs = discord.Embed(title=f"Ticket Service - {interaction.user.name}", description=f"{interaction.user.mention} a fermé un ticket service.\n\n*Ticket : {interaction.channel.mention}*", color=0xff0000)
                                EmbedTicketServiceClose = discord.Embed(title="Ticket fermé", description="Le ticket est fermé.\n\nPour le réouvrir, appuyez sur le bouton vert ci-dessous.\nPour le supprimer, appuyez sur le bouton rouge ci-dessous.", color=COLOR)

                                await transcript_channel.send(embed=EmbedTicketServiceCloseLogs)
                                await interaction.response.send_message("Le ticket a bien été fermé !", ephemeral=True)
                                await saveData(data)


                                # Boutons de l'embed TICKETSERVICECLOSE
                                class View_TicketServiceClose(discord.ui.View):

                                    # Bouton REOUVRIR
                                    @discord.ui.button(style=discord.ButtonStyle.green, label="Réouvrir")
                                    async def button_reopen(self, interaction: discord.Interaction, button_reopen: discord.ui.button):

                                        await interaction.message.delete()

                                        data = await getData()

                                        open_cat_id = 902038839860805675 # Catégorie des tickets ouverts
                                        transcript_channel_id = 1103402319200137217 # Channel des logs
                                        open_cat = await interaction.client.fetch_channel(str(open_cat_id))
                                        transcript_channel = interaction.client.get_channel(transcript_channel_id)

                                        EmbedTicketServiceReopen = discord.Embed(title="Rebonjour !", description="Le ticket a été réouvert !\n\n*Pour le fermer, veuillez appuyer sur le bouton ci-dessous.*", color=COLOR)
                                        msg = await interaction.channel.send(embed=EmbedTicketServiceReopen, view=View_TicketServiceWelcome())

                                        for ticket_id, ticket_user_id, msg_id in data["service"]["tickets"]["close"]:
                                            if ticket_id == interaction.channel.id:
                                                ticket_user = interaction.client.get_user(ticket_user_id)
                                                break
                                        
                                        await ticket_channel.set_permissions(ticket_role, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                                        await ticket_channel.set_permissions(ticket_user, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                        index = data["service"]["tickets"]["close"].index(list([interaction.channel.id, ticket_user_id, msg_id]))

                                        del data["service"]["tickets"]["close"][index]
                                        data["service"]["tickets"]["open"].append(tuple([interaction.channel.id, ticket_user_id, msg.id]))

                                        await interaction.channel.edit(category=open_cat)
                                        
                                        EmbedTicketServiceReopenLogs = discord.Embed(title=f"Ticket Service - {interaction.user.name}", description=f"{interaction.user.mention} a réouvert un ticket service.\n\n*Ticket : {interaction.channel.mention}*", color=0x32a852)
                                        await transcript_channel.send(embed=EmbedTicketServiceReopenLogs)

                                        await saveData(data)

                                        return await interaction.response.send_message("Le ticket a bien été réouvert !", ephemeral=True)

                                    # Bouton SUPPRIMER
                                    @discord.ui.button(style=discord.ButtonStyle.red, label="Supprimer")
                                    async def button_delete(self, interaction: discord.Interaction, button_delete: discord.ui.button):

                                        data = await getData()

                                        transcript_channel_id = 1103402319200137217 # Channel des logs
                                        transcript_channel = interaction.client.get_channel(transcript_channel_id)
                                        channel_id = interaction.channel.id

                                        with open(f"./database/tickets-transcripts/service/{ticket_channel.name}.txt", "a", encoding="UTF-8") as file:
                                            async for msg in ticket_channel.history(limit=None):
                                                file.write(f"{msg.created_at} - {msg.author.display_name} :\n    {msg.clean_content}\n")

                                        for ticket_id, ticket_user_id, msg_id in data["service"]["tickets"]["close"]:

                                            if ticket_id == channel_id:

                                                index = data["service"]["tickets"]["close"].index(list([channel_id, ticket_user_id, msg_id]))
                                                del data["service"]["tickets"]["close"][index]
                                                data["service"]["tickets_nb"]["total"] -= 1

                                                await interaction.channel.delete()

                                                EmbedTicketServiceDeleteLogs = discord.Embed(title=f"Ticket Service - {interaction.user.name}", description=f"{interaction.user.mention} a supprimé un ticket support.\n\n*Retrouvez le fichier texte de la sauvegarde ci-dessous.*", color=0xff0000)
                                                await transcript_channel.send(embed=EmbedTicketServiceDeleteLogs)
                                                
                                                file = discord.File(f"./database/tickets-transcripts/service/{interaction.channel.name}.txt") # Récupération du fichier
                                                await transcript_channel.send(file=file) # Envoie du fichier

                                                return await saveData(data)

                                await interaction.channel.send(embed=EmbedTicketServiceClose, view=View_TicketServiceClose())

                        await interaction.response.send_message(embed=EmbedTicketServiceCloseAsk, view=View_TicketServiceCloseAsk())
                        
                msg = await ticket_channel.send(embed=EmbedTicketServiceWelcome, view=View_TicketServiceWelcome())

                data["service"]["tickets_nb"]["total"] = tickets_nb
                data["service"]["tickets"]["open"].append(list([ticket_channel.id, interaction.user.id, msg.id]))
                await saveData(data)

                #EmbedTicketServiceVille = discord.Embed(title="Ticket - Service", description="Veuillez sélectionner votre ville.", color=COLOR)
                EmbedTicketServiceVille = discord.Embed(description="Veuillez sélectionner votre ville.", color=COLOR)

                options = [
                    discord.SelectOption(label="Draconiros", value="Draconiros"),
                    discord.SelectOption(label="Hellmina", value="Hellmina"),
                    discord.SelectOption(label="Tylezia", value="Tylezia"),
                    discord.SelectOption(label="Imagiro", value="Imagiro"),
                    discord.SelectOption(label="Orukam", value="Orukam"),
                    discord.SelectOption(label="Talkasha", value="Talkasha")
                ]


                class View_TicketServiceVille(discord.ui.View):

                    @discord.ui.select(
                        placeholder = "Choix du serveur...",
                        options = options
                    )

                    async def select_callback(self, interaction: discord.Interaction, select):

                        for ville in select.values:

                            data = await getData()

                            if ville in data["service"]["villes-prises"] :

                                await interaction.response.send_message("La ville sélectionnée est déjà privatisée.", ephemeral=False)
                            
                            elif ville == "Draconiros":

                                await interaction.response.send_message(f"Le serveur {ville} n'est plus disponible, il est déjà privatisé 🚫.", ephemeral=False)

                            else:

                                await interaction.response.send_message(f"Serveur : {ville}", ephemeral=True)

                                data = await getData()

                                data["service"]["tickets"][str(interaction.user.id)] = {
                                    "ville": str(ville)
                                }
                                data["service"]["tickets_nb"][str(ville)] += 1

                                await saveData(data)

                                #EmbedTicketServiceRarete = discord.Embed(title="Ticket - Service", description="Veuillez sélectionner la rareté du service.", color=COLOR)
                                EmbedTicketServiceRarete = discord.Embed(description="Veuillez sélectionner la catégorie.",color=COLOR)


                                class View_TicketServiceRarete(discord.ui.View):

                                    @discord.ui.button(label="Rare")
                                    async def button_rare(self, interaction: discord.Interaction, button_rare: discord.ui.button):

                                        await interaction.response.send_message(f"{ville}\nRare\n55M\nPar quel moyen souhaitez-vous régler ?", ephemeral=False)

                                    @discord.ui.button(label="Commun")
                                    async def button_commun(self, interaction: discord.Interaction, button_commun: discord.ui.Button):

                                        await interaction.response.send_message(f"{ville}\nCommun\n45M\nPar quel moyen souhaitez-vous régler ?", ephemeral=False)


                                    @discord.ui.button(label="Les deux")
                                    async def button_lesdeux(self, interaction: discord.Interaction, button_lesdeux: discord.ui.button):

                                        await interaction.response.send_message(f"{ville}\nRare + Commun\n80M\nPar quel moyen souhaitez-vous régler ?", ephemeral=False)

                                await msg2.edit(embed=EmbedTicketServiceRarete, view=View_TicketServiceRarete())

                msg2 = await ticket_channel.send(view=View_TicketServiceVille())

            # Bouton SUPPORT
            @discord.ui.button(style=discord.ButtonStyle.gray, label="❔ AUTRE")
            async def button_support(self, interaction: discord.Interaction, button_support: discord.ui.button):

                data = await getData()

                tickets_nb = data["support"]["tickets_nb"]
                tickets_nb += 1

                transcript_channel_id = 1103402319200137217 # Salon des logs
                ticket_role_id = 999539733459914844 # Rôle ayant les permissions de voir les tickets
                open_cat_id = 902038839860805675 # Catégorie des tickets ouverts

                transcript_channel = interaction.client.get_channel(transcript_channel_id)
                ticket_role = interaction.guild.get_role(int(ticket_role_id))
                open_cat = await interaction.client.fetch_channel(str(open_cat_id))
                ticket_channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-{tickets_nb}", category=open_cat)

                await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False, read_messages=False)
                await ticket_channel.set_permissions(interaction.user, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                await ticket_channel.set_permissions(ticket_role, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                await ticket_channel.send(f"{interaction.user.mention} {ticket_role.mention}")

                EmbedTicketSupportWelcome = discord.Embed(title="Bienvenue !", description="Nous sommes ravis que vous nous ayez contacté. Veuillez poser votre question et nous prendrons en charge votre demande dès que possible.", color=COLOR)
                EmbedTicketSupportLogs = discord.Embed(title=f"Ticket Support - {interaction.user.name}", description=f"{interaction.user.mention} a ouvert un ticket support.\n\n*Ticket : {ticket_channel.mention}*", color=0x32a852)

                await transcript_channel.send(embed=EmbedTicketSupportLogs)

                EmbedTicketSupportMessage = discord.Embed(title="Ticket - Support", description=f"Vous venez de créer un ticket support.\nVotre ticket : {ticket_channel.mention}", color=COLOR)
                await interaction.response.send_message(embed=EmbedTicketSupportMessage, ephemeral=True)


                # Boutons de l'embed TICKETSUPPORTWELCOME
                class View_TicketSupportWelcome(discord.ui.View):

                    # Bouton FERMER
                    @discord.ui.button(style=discord.ButtonStyle.red, label="Fermer")
                    async def button_closeask(self, interaction: discord.Interaction, button_closeask: discord.ui.button):

                        EmbedTicketSupportCloseAsk = discord.Embed(title="Ticket Support - Fermeture", description="Êtes-vous sûr de vouloir fermer le ticket ?", color=COLOR)

                        class View_TicketSupportCloseAsk(discord.ui.View):

                            @discord.ui.button(style=discord.ButtonStyle.red, label="Non")
                            async def button_closecancel(self, interaction: discord.Interaction, button_closecancel: discord.ui.button):

                                await interaction.message.delete()

                            @discord.ui.button(style=discord.ButtonStyle.green, label="Oui")
                            async def button_close(self, interaction: discord.Interaction, button_close: discord.ui.button):

                                await interaction.message.delete()

                                data = await getData()

                                close_cat_id = 972149365789564978 # Catégorie des tickets fermés
                                transcript_channel_id = 1103402319200137217 # Channel des logs
                                close_cat = await interaction.client.fetch_channel(str(close_cat_id))
                                transcript_channel = interaction.client.get_channel(transcript_channel_id)

                                for ticket_id, ticket_user_id, msg_id in data["support"]["tickets"]["open"]:
                                    if ticket_id == interaction.channel.id:
                                        ticket_user = interaction.client.get_user(ticket_user_id)
                                        msg = await interaction.channel.fetch_message(msg_id)
                                        break

                                await msg.delete()

                                await interaction.channel.set_permissions(ticket_user, view_channel=False, read_messages=False, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=False, external_emojis=False)

                                index = data["support"]["tickets"]["open"].index(list([interaction.channel.id, ticket_user_id, msg_id]))

                                del data["support"]["tickets"]["open"][index]
                                data["support"]["tickets"]["close"].append(tuple([interaction.channel.id, ticket_user_id, msg_id]))

                                await interaction.channel.edit(category=close_cat)

                                EmbedTicketSupportCloseLogs = discord.Embed(title=f"Ticket Support - {interaction.user.name}", description=f"{interaction.user.mention} a fermé un ticket support.\n\n*Ticket : {interaction.channel.mention}*", color=0xff0000)
                                EmbedTicketSupportClose = discord.Embed(title="Ticket fermé", description="Le ticket est fermé.\n\nPour le réouvrir, appuyez sur le bouton vert ci-dessous.\nPour le supprimer, appuyez sur le bouton rouge ci-dessous.", color=COLOR)

                                await transcript_channel.send(embed=EmbedTicketSupportCloseLogs)
                                await interaction.response.send_message("Le ticket a bien été fermé !", ephemeral=True)
                                await saveData(data)


                                # Boutons de l'embed TICKETSUPPORTCLOSE
                                class View_TicketSupportClose(discord.ui.View):

                                    # Bouton REOUVRIR
                                    @discord.ui.button(style=discord.ButtonStyle.green, label="Réouvrir")
                                    async def button_reopen(self, interaction: discord.Interaction, button_reopen: discord.ui.button):

                                        await interaction.message.delete()

                                        data = await getData()

                                        open_cat_id = 902038839860805675 # Catégorie des tickets ouverts
                                        transcript_channel_id = 1103402319200137217 # Channel des logs
                                        open_cat = await interaction.client.fetch_channel(str(open_cat_id))
                                        transcript_channel = interaction.client.get_channel(transcript_channel_id)

                                        EmbedTicketSupportReopen = discord.Embed(title="Rebonjour !", description="Le ticket a été réouvert !\n\n*Pour le fermer, veuillez appuyer sur le bouton ci-dessous.*", color=COLOR)
                                        msg = await interaction.channel.send(embed=EmbedTicketSupportReopen, view=View_TicketSupportWelcome())

                                        for ticket_id, ticket_user_id, msg_id in data["support"]["tickets"]["close"]:
                                            if ticket_id == interaction.channel.id:
                                                ticket_user = interaction.client.get_user(ticket_user_id)
                                                break
                                        
                                        await ticket_channel.set_permissions(ticket_role, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                                        await ticket_channel.set_permissions(ticket_user, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                                        index = data["support"]["tickets"]["close"].index(list([interaction.channel.id, ticket_user_id, msg_id]))

                                        del data["support"]["tickets"]["close"][index]
                                        data["support"]["tickets"]["open"].append(tuple([interaction.channel.id, ticket_user_id, msg.id]))

                                        await interaction.channel.edit(category=open_cat)
                                        
                                        EmbedTicketSupportReopenLogs = discord.Embed(title=f"Ticket Support - {interaction.user.name}", description=f"{interaction.user.mention} a réouvert un ticket support.\n\n*Ticket : {interaction.channel.mention}*", color=0x32a852)
                                        await transcript_channel.send(embed=EmbedTicketSupportReopenLogs)

                                        await saveData(data)

                                        return await interaction.response.send_message("Le ticket a bien été réouvert !", ephemeral=True)

                                    # Bouton SUPPRIMER
                                    @discord.ui.button(style=discord.ButtonStyle.red, label="Supprimer")
                                    async def button_delete(self, interaction: discord.Interaction, button_delete: discord.ui.button):

                                        data = await getData()

                                        transcript_channel_id = 1103402319200137217 # Channel des logs
                                        transcript_channel = interaction.client.get_channel(transcript_channel_id)
                                        channel_id = interaction.channel.id

                                        with open(f"./database/tickets-transcripts/support/{ticket_channel.name}.txt", "a", encoding="UTF-8") as file:
                                            async for msg in ticket_channel.history(limit=None):
                                                file.write(f"{msg.created_at} - {msg.author.display_name} :\n    {msg.clean_content}\n")

                                        for ticket_id, ticket_user_id, msg_id in data["support"]["tickets"]["close"]:

                                            if ticket_id == channel_id:

                                                index = data["support"]["tickets"]["close"].index(list([channel_id, ticket_user_id, msg_id]))
                                                del data["support"]["tickets"]["close"][index]
                                                data["support"]["tickets_nb"] -= 1

                                                await interaction.channel.delete()

                                                EmbedTicketSupportDeleteLogs = discord.Embed(title=f"Ticket Support - {interaction.user.name}", description=f"{interaction.user.mention} a supprimé un ticket support.\n\n*Retrouvez le fichier texte de la sauvegarde ci-dessous.*", color=0xff0000)
                                                await transcript_channel.send(embed=EmbedTicketSupportDeleteLogs)
                                                
                                                file = discord.File(f"./database/tickets-transcripts/support/{interaction.channel.name}.txt") # Récupération du fichier
                                                await transcript_channel.send(file=file) # Envoie du fichier

                                                return await saveData(data)

                                await interaction.channel.send(embed=EmbedTicketSupportClose, view=View_TicketSupportClose())

                        await interaction.response.send_message(embed=EmbedTicketSupportCloseAsk, view=View_TicketSupportCloseAsk())

                msg = await ticket_channel.send(embed=EmbedTicketSupportWelcome, view=View_TicketSupportWelcome())

                data["support"]["tickets_nb"] = tickets_nb
                data["support"]["tickets"]["open"].append(list([ticket_channel.id, interaction.user.id, msg.id]))
                await saveData(data)

        await support_channel.send(embed=EmbedTicket, view=View_Ticket())


async def setup(client):
    await client.add_cog(ticket(client))