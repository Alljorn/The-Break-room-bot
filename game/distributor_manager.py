from game.data.data_base import DATA_BASE
from game.supply_manager import SupplyManager
from game.exceptions import DistributorAlreadyExist,DistributorNotExist, SupplyNotExist, SupplyNotInInventory


class DistributorManager:
    """
    Le Distributor Manager permet de gérer les données des distributeurs

    Méthodes de classe:
        - add_supply_to_inventory_of(distributor_id, supply_name): ajoute un produit à l'inventaire d'un distributeur
        - delete_distributor(distributor_id): supprime un distributeur
        - distributor_exist(distributor_id); vérifie qu'un distributeur existe via son identifiant
        - get_distributor(distributor_id): donne les données d'un distributeur via son identifiant
        - get_from_inventory_of(distributor_id, supply_name): donne le slot du produit dans l'inventaire d'un distributeur
        - get_inventory_of(distributor_id): donne l'inventaire d'un distributeur
        - get_quantity_from_inventory_of(distributor_id, supply_name): donne la quantité d'un produit possédé par un distributeur
        - new_distributor(distributor_id): crée un distributeur
        - remove_from_inventory_of(distributor_id, supply_name): enlève un produit de l'inventaire d'un distributeur
        - supply_in_inventory_of(distributor_id, supply_name): vérifie qu'un produit est présent dans l'inventaire d'un distributeur
    """

    @staticmethod
    def get_distributor(distributor_id: int) -> tuple:
        """
        Donne les données d'un distributeur via son identifiant
        Argument:
            distributor_id: int 
            | L'identifiant du distributeur
        Excpetion:
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie un tuple contenant les données du distributeur
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL séléctionant l'entrée dans la base de données du distributeur
        response = cursor.execute(f"SELECT * FROM distributor WHERE id == {distributor_id}")
        user_data = response.fetchone() # On récupére les données

        if user_data is None: raise DistributorNotExist(distributor_id)
        return user_data

    @staticmethod
    def distributor_exist(distributor_id: int) -> bool:
        """
        Vérifie qu'un distributeur existe via son identifiant
        Argument:
            distributor_id: int 
            | L'identifiant du distributeur
        
        renvoie True si le distributeur existe, False sinon
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"

        try :
            DistributorManager.get_distributor(distributor_id)
            return True
        except DistributorNotExist:
            return False

    @staticmethod
    def new_distributor(distributor_id: int) -> None:
        """
        Crée un distributeur
        Argument:
            distributor_id: int 
            | L'identifiant du distributeur
        Exception:
            | DistributorAreadyExist: si le distributeur existe déjà
        
        ne renvoie rien
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if DistributorManager.distributor_exist(distributor_id): raise DistributorAlreadyExist(distributor_id)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL ajoutant le distributeur avec les paramètres par défaut
        cursor.execute(f"""
                        INSERT INTO distributor(id)
                        VALUES ({distributor_id});""")
        DATA_BASE.commit() # Met à jour la base de données

    @staticmethod
    def delete_distributor(distributor_id: int) -> None:
        """
        Supprime un distributeur
        Argument:
            distributor_id: int 
            | L'identifiant du distributeur
        Exception:
            - DistributorNotExist: si le distributeur n'existe pas
        
        ne renvoie rien
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL effaçant l'entrée de le distributeur de la base de données
        cursor.execute(f"""
                        DELETE FROM distributor
                        WHERE id == {distributor_id};
                        """)
        DATA_BASE.commit() # Met à jour la base de données


    # Inventory Management
    @staticmethod
    def get_from_inventory_of(distributor_id: int, supply_name: str) -> tuple:
        """
        Donne le slot du produit dans l'inventaire d'un distributeur
        Arguments:
            distributor_id: int 
            | L'identifiant du distributeur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - DistributorNotExist: si le distrbuteur n'existe pas
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si le distributeur ne posséde pas le poduit

        renvoie un tuple contenant le nom du produit et la quantité possédée par le distributeur
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL donnant le nom du produit et la quantité possédée par le distributeur
        response = cursor.execute(f"""
                                   SELECT content, quantity
                                   FROM distributor_inventory
                                   WHERE id == {distributor_id} and content == "{supply_name}";
                                   """)
        slot = response.fetchone() # On récupère les données

        if slot is None: raise SupplyNotInInventory(distributor_id, supply_name)
        return slot

    @staticmethod
    def supply_in_inventory_of(distributor_id: int, supply_name: str) -> bool:
        """
        Vérifie qu'un produit est présent dans l'inventaire d'un distributeur
        Arguments:
            distributor_id: int 
            | L'identifiant du distributeur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - DistributorNotExist: si le distributeur n'existe pas
            - SupplyNotExist: si le produit n'existe pas

        renvoie True si le distributeur posséde le produit, False sinon
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        try:
            DistributorManager.get_from_inventory_of(distributor_id, supply_name)
            return True
        except SupplyNotInInventory:
            return False

    @staticmethod
    def get_inventory_of(distributor_id: int) -> list:
        """
        Donne l'inventaire d'un distributeur
        Argument:
            distributor_id: int 
            | L'identifiant du distributeur
        Exception:
            - DistributorNotExist: si le distributeur n'existe pas

        renvoie une liste contenant les noms des produits et leurs quantités possédés par le distributeur
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant les noms des produits possédés par le distributeur
        response = cursor.execute(f"""
                                   SELECT content, quantity
                                   FROM distributor_inventory
                                   WHERE id == {distributor_id};
                                   """)
        return response.fetchall() # On récupère les données

    @staticmethod
    def get_quantity_from_inventory_of(distributor_id: int, supply_name: str) -> int:
        """
        Donne la quantité d'un produit possédé par un distributeur
        Arguments:
            distributor_id: int 
            | L'identifiant du distributeur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - DistributorNotExist: si le distributeur n'existe pas
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si le distributeur ne posséde pas le poduit

        renvoie la quantité du produit possédé par le distributeur
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupère les informations du slot
        slot = DistributorManager.get_from_inventory_of(distributor_id, supply_name)
        
        return slot[1] # On renvoie la quantité

    @staticmethod
    def add_supply_to_inventory_of(distributor_id: int, supply_name: str) -> None:
        """
        Ajoute un produit à l'inventaire d'un distributeur
        Arguments:
            distributor_id: int 
            | L'identifiant du distributeur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - DistributorNotExist: si le distributeur n'existe pas
            - SupplyNotExist: si le produit n'existe pas
        
        ne renvoie rien
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Si le distributeur ne posséde pas le produit
        if not DistributorManager.supply_in_inventory_of(distributor_id, supply_name):
            # On ajoute le produit à l'inventaire
            cursor.execute(f"""
                            INSERT INTO distributor_inventory (id, content)
                            VALUES ({distributor_id}, "{supply_name}");
                            """)
        else:
            # On incrémente la quantité du produit possédé
            cursor.execute(f"""
                        UPDATE distributor_inventory
                        SET quantity = quantity + 1
                        WHERE id == {distributor_id} and content == "{supply_name}";
                        """)
        DATA_BASE.commit() # Met à jour la bse de données

    @staticmethod
    def remove_from_inventory_of(distributor_id: int, supply_name: str) -> None:
        """
        Enlève un produit de l'inventaire d'un distributeur
        Arguments:
            distributor_id: int 
            | L'identifiant du distributeur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - DistributorNotExist: si le distributeur n'existe pas
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si le distributeur ne posséde pas le poduit

        ne renvoie rien
        """
        assert type(distributor_id) == int, "distributor_id agument must be int"
        if not DistributorManager.distributor_exist(distributor_id): raise DistributorNotExist(distributor_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        if not DistributorManager.supply_in_inventory_of(distributor_id, supply_name): raise SupplyNotInInventory(distributor_id, supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Décrémente la quantité du produit possédé
        cursor.execute(f"""
                        UPDATE distributor_inventory
                        SET quantity = quantity - 1
                        WHERE id == {distributor_id} and content == "{supply_name}";
                        """)
        # Si la quanité possédé atteind zéro
        if DistributorManager.get_quantity_from_inventory_of(distributor_id, supply_name) <= 0:
            # On supprime le slot
            cursor.execute(f"""
                            DELETE FROM distribuor_inventory
                            WHERE id == {distributor_id} and content == "{supply_name}";
                            """)
        DATA_BASE.commit() # Met à jour la base de données