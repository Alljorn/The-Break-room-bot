import sqlite3

from game.data.data_base import DATA_BASE
from game.supply_manager import SupplyManager
from game.exceptions import UserAlreadyExist,UserNotExist,RoleNotReferenced, SupplyNotExist, SupplyNotInInventory



class UserManager:
    """
    L'User Manager permet de gérer les données des utilisateurs

    Méthodes de classe:
        - add_supply_to_inventory_of(user_id, supply_name): ajoute un produit à l'inventaire d'un utilisateur
        - change_use_role(user_id, role_name): change le rôle d'un utilisateur
        - delete_user(user_id): supprime un uilisateur
        - get_from_inventory_of(user_id, supply_name): donne le slot du produit dans l'inventaire d'un utilisateur
        - get_inventoy_of(user_id): donne l'inventaire d'un utilisateur
        - get_money_of(user_id): donne le montant de l'agent d'un utilisateu via son id
        - get_permission_level(role_name): donne le niveau de permision d'un rôle référencé
        - get_role_of(user_id): donne le rôle d'un utilisteur via son identifiant
        - get_roles_ref(): donne les rôles référencés par l'User Manager
        - get_quantity_from_inventory_of(user_id, supply_name): donne la quantité d'un produit possédé par un utilisateur
        - get_user(user_id): donne les données d'un utilisateur via son identifiant
        - remove_from_inventory_of(user_id): enlève un produit de l'inventaire d'un utilisateur
        - role_exist(role): vérifie qu'un rôle est référencé par l'User Manager
        - set_money_of(user_id, money): change le montant de l'agent d'un utilisateu via son id
        - supply_in_inventory_of(user_id, supply_name): vérifie qu'un produit est présent dans l'inventaire d'un utilisateur
        - user_exist(user_id): vérifie qu'un utilisteur existe via son identifiant
        - new_user(user_id): crée un utilisateur
    """
 
    @staticmethod
    def get_user(user_id: int) -> tuple:
        """
        Donne les données d'un utilisateur via son identifiant
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Excpetion:
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie un tuple contenant les données de l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL séléctionant l'entrée dans la base de données de l'utilisateur
        response = cursor.execute(f"SELECT * FROM user WHERE id == {user_id}")
        user_data = response.fetchone() # On récupére les données

        if user_data is None: raise UserNotExist(user_id)
        return user_data
 
    @staticmethod
    def user_exist(user_id: int) -> bool:
        """
        Vérifie qu'un utilisteur existe via son identifiant
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        
        renvoie True si l'utilisateur existe, False sinon
        """
        assert type(user_id) == int, "user_id agument must be int"

        try :
            UserManager.get_user(user_id)
            return True
        except UserNotExist:
            return False

    @staticmethod
    def new_user(user_id: int) -> None:
        """
        Crée un utilisateur
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Exceptions:
            | UserAreadyExist: si l'utilisateur existe déjà
            | RoleNotReferenced: si le rôle pr défaut n'est pas référencé
        
        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        if UserManager.user_exist(user_id): raise UserAlreadyExist(user_id)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Requête SQL ajoutant l'utilisateur avec les paramètres par défaut
            cursor.execute(f"""
                            INSERT INTO user(id)
                            VALUES ({user_id});""")
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            raise RoleNotReferenced("classic")   

    @staticmethod
    def delete_user(user_id: int) -> None:
        """
        Supprime un utilisateur
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL effaçant l'entrée de l'utilisateur de la base de données
        cursor.execute(f"""
                        DELETE FROM user
                        WHERE id == {user_id};
                        """)
        DATA_BASE.commit() # Met à jour la base de données


    # Role Managemnt
    @staticmethod
    def get_roles_ref() -> list[tuple]:
        """
        Donne les rôles référencés par l'User Manager
        
        renvoie une liste de tuple contenant les rôles référencés par l'User Manager
        """
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL qui récupére le nom de tout les rôles référencés
        response = cursor.execute("""
                                  SELECT name
                                  FROM roles_ref;
                                  """)
        return response.fetchall()
    
    @staticmethod
    def get_role_of(user_id: int) -> str:
        """
        Donne le rôle d'un utilisteur via son identifiant
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        renvoie un str correspondant au rôle de l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le rôle de l'utilisateu
        response = cursor.execute(f"""
                                   SELECT role
                                   FROM user 
                                   WHERE id == {user_id};
                                   """)
        role = response.fetchone() # On récupére les données

        if role is None: raise UserNotExist(user_id)
        return role[0]

    @staticmethod
    def role_exist(role_name: str) -> bool:
        """
        Vérifie qu'un rôle est référencé par l'User Manager
        Argument:
            role_name: str
            | Le rôle à vérifié
        
        renvoie True si le rôle est référencé, False sinon
        """
        assert type(role_name) == str, "role_name agument must be str"

        for role_ref in UserManager.get_roles_ref():
            if role_name in role_ref: return True
        return False
    
    @staticmethod
    def get_permission_level_of(role_name: str) -> int:
        """
        Donne le niveau de permision d'un rôle référencé
        Argument:
            role_name: str
            | Le nom du rôle
        Exception:
            - RoleNotReferenced: si le rôle n'est pas référencé par le User Manager
        
        renvoie le niveau de pemision du rôle (int)
        """
        assert type(role_name) == str, "role_name agument must be str"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le niveau de permission du rôle
        response = cursor.execute(f"""
                                   SELECT level_permissio
                                   FROM roles_ref
                                   WHERE name == '{role_name}';
                                   """)
        level_permission = response.fetchone() # On récupére les données
        
        if level_permission is None: raise RoleNotReferenced(role_name)
        return  level_permission[0]

    @staticmethod
    def change_user_role(user_id: int, role_name: str) -> tuple:
        """
        Change le rôle d'un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            role_name: str
            | Le nouveau rôle de l'utilisateur
        Exceptions:
            - UserNotExist: si l'utilisateur n'existe pas
            - RoleNotReferenced: si le rôle n'est pas référencé par le User Manager
        
        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        assert type(role_name) == str, "role_name agument must be str"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Requête SQL changeant le rôle de l'utilisateur
            cursor.execute(f"""
                            UPDATE user
                            SET role = '{role_name}'
                            WHERE id == {user_id};
                            """)
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            raise RoleNotReferenced(role_name)
    
    
    # Money Management
    @staticmethod
    def get_money_of(user_id: int) -> int:
        """
        Donne le montant de l'agent d'un utilisateu via son id
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        renvoie le montant de l'argent de l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le montant de l'agent de l'utilisateur
        response = cursor.execute(f"""
                                   SELECT money
                                   FROM user
                                   WHERE id == {user_id};
                                   """)
        money = response.fetchone() # On récupére les données

        if money is None: raise UserNotExist(user_id)
        return money[0]
    
    @staticmethod
    def set_money_of(user_id: int, money: int) -> int:
        """
        Change le montant de l'agent d'un utilisateu via son id
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            money: int
            | Le montant de l'argent à définir
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(money) == int, "money agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL changent le montant de l'agent de l'utilisateur
        cursor.execute(f"""
                        UPDATE user
                        SET money = {money}
                        WHERE id == {user_id};
                        """)
        DATA_BASE.commit() # Met à jour la base de données
    

    # Inventory Management
    @staticmethod
    def get_from_inventory_of(user_id: int, supply_name: str) -> tuple:
        """
        Donne le slot du produit dans l'inventaire d'un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si l'utilisateur ne posséde pas le poduit
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie un tuple contenant le nom du produit et la quantité possédée par l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL donnant le nom du produit et la quantité possédée par l'utilisateur
        response = cursor.execute(f"""
                                   SELECT content, quantity
                                   FROM user_inventory
                                   WHERE id == {user_id} and content == "{supply_name}";
                                   """)
        slot = response.fetchone() # On récupère les données

        if slot is None: raise SupplyNotInInventory(user_id, supply_name)
        return slot
    
    @staticmethod
    def supply_in_inventory_of(user_id: int, supply_name: str) -> bool:
        """
        Vérifie qu'un produit est présent dans l'inventaire d'un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - SupplyNotExist: si le produit n'existe pas
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie True si l'utilisateur posséde le produit, False sinon
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        try:
            UserManager.get_from_inventory_of(user_id, supply_name)
            return True
        except SupplyNotInInventory:
            return False

    @staticmethod
    def get_inventory_of(user_id: int) -> list:
        """
        Donne l'inventaire d'un utilisateur
        Argument:
            user_id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie une liste contenant les noms des produits et leurs quantités possédés par l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant les noms des produits possédés par l'utilisateur
        response = cursor.execute(f"""
                                   SELECT content, quantity
                                   FROM user_inventory
                                   WHERE id == {user_id};
                                   """)
        return response.fetchall() # On récupère les données
    
    @staticmethod
    def get_quantity_from_inventory_of(user_id: int, supply_name: str) -> int:
        """
        Donne la quantité d'un produit possédé par un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si l'utilisateur ne posséde pas le poduit
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie la quantité du produit possédé par l'utilisateur
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupère les informations du slot
        slot = UserManager.get_from_inventory_of(user_id, supply_name)
        
        return slot[1] # On renvoie la quantité

    @staticmethod
    def add_supply_to_inventory_of(user_id: int, supply_name: str) -> None:
        """
        Ajoute un produit à l'inventaire d'un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - SupplyNotExist: si le produit n'existe pas
            - UserNotExist: si l'utilisateur n'existe pas
        
        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Si l'utilisateur ne posséde pas le produit
        if not UserManager.supply_in_inventory_of(user_id, supply_name):
            # On ajoute le produit à l'inventaire
            cursor.execute(f"""
                            INSERT INTO user_inventory (id, content)
                            VALUES ({user_id}, "{supply_name}");
                            """)
        else:
            # On incrémente la quantité du produit possédé
            cursor.execute(f"""
                        UPDATE user_inventory
                        SET quantity = quantity + 1
                        WHERE id == {user_id} and content == "{supply_name}";
                        """)
        DATA_BASE.commit() # Met à jour la bse de données

    @staticmethod
    def remove_from_inventory_of(user_id: int, supply_name: str) -> None:
        """
        Enlève un produit de l'inventaire d'un utilisateur
        Arguments:
            user_id: int 
            | L'identifiant de l'utilisateur
            supply_name: str
            | Le nom du produit
        Exceptions:
            - SupplyNotExist: si le produit n'existe pas
            - SupplyNotInInventory: si l'utilisateur ne posséde pas le poduit
            - UserNotExist: si l'utilisateur n'existe pas

        ne renvoie rien
        """
        assert type(user_id) == int, "user_id agument must be int"
        if not UserManager.user_exist(user_id): raise UserNotExist(user_id)
        assert type(supply_name) == str, "supply_name agument must be str"
        if not SupplyManager.supply_exist(supply_name): raise SupplyNotExist(supply_name)

        if not UserManager.supply_in_inventory_of(user_id, supply_name): raise SupplyNotInInventory(user_id, supply_name)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Décrémente la quantité du produit possédé
        cursor.execute(f"""
                        UPDATE user_inventory
                        SET quantity = quantity - 1
                        WHERE id == {user_id} and content == "{supply_name}";
                        """)
        # Si la quanité possédé atteind zéro
        if UserManager.get_quantity_from_inventory_of(user_id, supply_name) <= 0:
            # On supprime le slot
            cursor.execute(f"""
                            DELETE FROM user_inventory
                            WHERE id == {user_id} and content == "{supply_name}";
                            """)
        DATA_BASE.commit() # Met à jour la base de données