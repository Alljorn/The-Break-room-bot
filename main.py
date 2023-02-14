import discord
import config.timeout
from config.token import token

from game.user_manager import UserManager
from game.distributor_manager import DistributorManager
from game.supply_manager import SupplyManager


bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt")

@bot.slash_command(name = "faire_une_pause", description = "Prenez une pause, commande principale")
async def take_a_break(ctx: discord.ApplicationContext):
    if not UserManager.user_exist(ctx.author.id):
        message = "Félicitation vous êtes embauché !\nCréer une partie ?"
        class create_game_view(discord.ui.View):

            @discord.ui.button(label="J'accepte", style=discord.ButtonStyle.green)
            async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                UserManager.new_user(ctx.author.id)
                message = "Encore félicitation !"
                self.disable_on_timeout = False
                await interaction.response.edit_message(content=message, view=None)
            
            @discord.ui.button(label="Je refuse", style=discord.ButtonStyle.red)
            async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                message = "Une autre occasion se présentera"
                await interaction.response.edit_message(content=message, view=None)
        await ctx.respond(message, view = create_game_view(timeout=config.timeout.CREATE_GAME, disable_on_timeout=True))
    else:
##########-------------------------- DISTRIBUTEUR --------------------------##########
        class distributor_embed(discord.Embed):
            """
            L'embed d'affichage du distributeur
            """
            def __init__(self):
                super().__init__( # Création de l'embed
                    title="Distibuteur", 
                    description="Des nouveautés ?"
                )
                # Si le distributeur à afficher n"existe pas
                if not DistributorManager.distributor_exist(ctx.author.id):
                    self.add_field( # message d'information
                        name="Aucun distributeur",
                        value="Votre entreprise ne possède aucun distributeur, ce n'est pas normal"
                    )
                # Si le distributeur à afficher existe
                else:
                    # On récupère son inventaire
                    distributor_inventory = DistributorManager.get_inventory_of(ctx.author.id)
                    # Affichage de l'inventaire du distributeur
                    if distributor_inventory == []: # si il est vide
                        self.add_field( # message d'information
                            name="Le distributeur est vide",
                            value="Temps avant remplissage: " + "undef"
                        )
                    else:
                        # Pour chaque produit de l'inventaire
                        for supply in distributor_inventory:
                            supply = SupplyManager.get_supply(supply[0]) # récupère les informations sur le produit
                            self.add_field( # affichage du nom et du prix
                                name=supply[0],
                                value='prix: ' + str(supply[2]) + '$'
                            )
        class distributor_view(discord.ui.View):
            """
            Le menu de navigation du distributeur.
            """

            async def on_timeout(self) -> None:
                UserManager.set_status_of(ctx.author.id, True)
                self.disable_all_items()
                await ctx.interaction.edit_original_response(view=self)
            

            # Si le distributeur existe
            if DistributorManager.distributor_exist(ctx.author.id):
                # Création d'un menu de selection
                @discord.ui.select(
                    placeholder = "Souaitez-vous acheter quelque chose ?", # titre
                    # nombre de choix minimum et maximum
                    min_values = 1,
                    max_values=1,
                    # ajout des options
                    options = [
                        discord.SelectOption(
                            label="Quitter",
                            description="Retourner à la salle de pause"
                        )]
                        + [
                        discord.SelectOption( # choix d'achat des produits de l'inventaire du ditributeur
                            label=supply[0], # le nom
                            description=str(SupplyManager.get_supply(supply[0])[2]) + '$' # le prix
                        ) for supply in DistributorManager.get_inventory_of(ctx.author.id)
                    ]
                )
                async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                    """
                    Est appelé quand un choix à été fait 
                    """
                    # Si on veut quitter le ditributeur
                    if select.values[0] == "Quitter":
                        self.on_timeout = super().on_timeout
                        await interaction.response.edit_message(embed = break_room_embed(), view = break_room_view(timeout=config.timeout.BREAK_ROOM))
                    else: # Sinon un choix d'achat a été fait
                        ###
                        debug = False # Mettre la variable à True pour activer les messages de debug, False sinon
                        ###
                        debug_message = f"[DEBUG] Achat en cours de **{select.values[0]}** ...\n"
                        # On récupère les informations nécessaire aux oppérations
                        user_money = UserManager.get_money_of(ctx.author.id) # la quantité de monnaie que l'utilisateur possède
                        prix = SupplyManager.get_supply(select.values[0])[2] # le prix du produit choisit
                        debug_message += f"inventaire:\n{UserManager.get_inventory_of(ctx.author.id)}"
                        debug_message += f"[DEBUG] user_money: {user_money}  |  prix: {prix}$\n"
                        # Message d'échec 
                        embed = discord.Embed(title="Achat annulé", description=f"Solde insuffisant à l'achat de **{select.values[0]}**")
                        # On vérifie que l'utilisateur peut acheté le produit
                        if user_money < prix:
                            debug_message += f"[DEBUG] Solde insuffisant, l'achat de **{select.values[0]}** est annulé\n"
                        else:
                            # Payement
                            UserManager.set_money_of(ctx.author.id, user_money-prix)
                            user_money -= prix
                            debug_message += f"[DEBUG] -{prix}$ |  user_money: {user_money}\n"
                            # Obtention du produit
                            DistributorManager.remove_from_inventory_of(ctx.author.id, select.values[0])
                            UserManager.add_supply_to_inventory_of(ctx.author.id, select.values[0])
                            debug_message += f"[DEBUG] **{select.values[0]}** a été retiré du distributeur et ajouté à l'inventaire\n"
                            debug_message += f"inventaire:\n{UserManager.get_inventory_of(ctx.author.id)}\n"
                            
                            # Message de succès
                            embed = discord.Embed(title="Achat effectué !", description=f"Vous avez acheté **{select.values[0]}**")
                        # L'utilisateur redevient actif
                        UserManager.set_status_of(ctx.author.id, True)
                        # Affichage du résultat
                        self.on_timeout = super().on_timeout
                        await interaction.response.edit_message(content=debug_message if debug else "", view=None, embed=embed)
##########----------------------------- BUREAU -----------------------------##########
        class office_embed(discord.Embed):
            def __init__(self):
                super().__init__(
                    title = "Vous voilà devant votre bureau",
                    description="Choisissez une tâche à accomplir"
                )
                self.add_field(
                    name = "Tâches en cours:",
                    value = "vide",
                    inline = False
                )
                self.add_field(
                    name = "Tâches disponibles:",
                    value = "vide",
                    inline = False
                )
        class office_view(discord.ui.View):

            async def on_timeout(self) -> None:
                UserManager.set_status_of(ctx.author.id, True)
                self.disable_all_items()
                await ctx.interaction.edit_original_response(view=self)
            
            @discord.ui.select(
                placeholder = "Que voulez-vous faire ?",
                min_values = 1,
                max_values = 1,
                options = {
                    discord.SelectOption(
                            label="Quitter",
                            description="Retourner à la salle de pause"
                        )
                }
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                """
                Est appelé quand un choix à été fait 
                """
                # Si on veut quitter le bureau
                if select.values[0] == "Quitter":
                    self.on_timeout = super().on_timeout
                    await interaction.response.edit_message(embed = break_room_embed(), view = break_room_view(timeout=config.timeout.BREAK_ROOM))
##########------------------------- SALLE DE PAUSE -------------------------##########
        class break_room_embed(discord.Embed):
            def __init__(self):
                super().__init__( 
                    title = "Bienvenue dans la salle de pause",
                    description = "Cette atmosphère réconfortante vous appaise"
                )
                self.add_field(
                    name = "Tâches en cours:",
                    value = "vide",
                    inline = False
                )
                self.add_field(
                    name = "Rapport de travail:",
                    value = "vide",
                    inline = False
                )
        class break_room_view(discord.ui.View):

            async def on_timeout(self) -> None:
                UserManager.set_status_of(ctx.author.id, True)
                self.disable_all_items()
                await ctx.interaction.edit_original_response(view=self)
        
            @discord.ui.select(
                placeholder = "Où souhaitez-vous aller ?",
                min_values = 1,
                max_values = 1,
                options = [
                    discord.SelectOption(
                        label="Distributeur",
                        description="Achetez tout un tas de chose !"
                    ),
                    discord.SelectOption(
                        label="Bureau",
                        description="Retournez travailler dans votre bureau"
                    )
                ]

            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                if select.values[0] == "Distributeur":
                    self.on_timeout = super().on_timeout
                    await interaction.response.edit_message(embed = distributor_embed(), view = distributor_view(timeout=config.timeout.DISTRIBUTOR))
                elif select.values[0] == "Bureau":
                    self.on_timeout = super().on_timeout
                    await interaction.response.edit_message(embed = office_embed(), view = office_view(timeout=config.timeout.OFFICE))
        
        print(UserManager.is_active(ctx.author.id))
        # L'utiliateur est maintenant en pause
        UserManager.set_status_of(ctx.author.id, False)
        # Envoie du menu de séléction
        await ctx.respond(embed = break_room_embed(), view = break_room_view(timeout=config.timeout.BREAK_ROOM))


bot.run(token)
