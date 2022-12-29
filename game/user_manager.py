import sqlite3

from game.data_base import DATA_BASE
from game.exceptions import UserAlreadyExist,UserNotExist,RoleNotReferenced

from config.game import DEFAULT_USER_ROLE, DEFAULT_USER_MONEY


class UserManager:
    """
    L'User Manager permet de gérer les données des utilisateur

    Méthodes de classe:
        - change_use_role(id, role): change le rôle d'un utilisateur
        - delete_user(id): supprime un uilisateur
        - get_money_of(id): donne le montant de l'agent d'un utilisateu via son id
        - get_permission_level(role): donne le niveau de permision d'un rôle référencé
        - get_role_of(id): donne le rôle d'un utilisteur via son identifiant
        - get_roles_ref(): donne les rôles référencés par l'User Manager
        - get_user(id): donne les données d'un utilisateur via son identifiant
        - set_money_of(id, money): change le montant de l'agent d'un utilisateu via son id
        - user_exist(id): vérifie qu'un utilisteur existe via son identifiant
        - new_user(id): crée un utilisateur
    """

    def __init_roles_ref() -> None:
        """
        Initialise les rôles référencés dans la base données

        ne renvoie rien
        """
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # On ajoute les différents rôles référencés
        try: cursor.execute("INSERT INTO roles_ref VALUES('administrator', 0);")
        except sqlite3.IntegrityError: pass    
        try: cursor.execute("INSERT INTO roles_ref VALUES('classic', 1);")
        except sqlite3.IntegrityError: pass 
        DATA_BASE.commit() # Met à jour la base de données
    __init_roles_ref()

    @staticmethod
    def get_roles_ref() -> tuple:
        """
        Donne les rôles référencés par l'User Manager
        
        renvoie un tuple contenant les rôles référencés pr l'User Manager
        """
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL qui récupére le nom de tout les rôles référencés
        response = cursor.execute("SELECT name FROM roles_ref;")
        return response.fetchall()
        
    @staticmethod
    def get_user(id: int) -> tuple:
        """
        Donne les données d'un utilisateur via son identifiant
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Excpetion:
            - UserNotExist: si l'utilisateur n'existe pas

        renvoie un tuple contenant les données de l'utilisateur
        """
        assert type(id) == int, "id agument must be int"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL séléctionant l'entrée dans la base de données de l'utilisateurr
        response = cursor.execute(f"SELECT * FROM user WHERE id == {id}")
        user_data = response.fetchone() # On récupére les données

        if user_data is None: raise UserNotExist(id)
        return user_data

    
    @staticmethod
    def user_exist(id: int) -> bool:
        """
        Vérifie qu'un utilisteur existe via son identifiant
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        
        renvoie True si l'utilisateur existe, False sinon
        """
        try :
            UserManager.get_user(id)
            return True
        except UserNotExist:
            return False


    @staticmethod
    def new_user(id: int) -> tuple:
        """
        Crée un utilisateur
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Exceptions:
            | UserAreadyExist: si l'utilisateur existe déjà
            | RoleNotReferenced: si le rôle pr défaut n'est pas référencé
        
        renvoie un tuple contenant les informations de l'utilisteur créé
        """
        assert type(id) == int, "id agument must be int"
        if UserManager.user_exist(id): raise UserAlreadyExist(id)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Requête SQL ajoutant l'utilisateur avec les paramètres par défaut
            cursor.execute(f"INSERT INTO user VALUES({id}, '{DEFAULT_USER_ROLE}', {DEFAULT_USER_MONEY});")
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            raise RoleNotReferenced(DEFAULT_USER_ROLE)
        # Récupére les données de l'utilisateur créé
        return UserManager.get_user(id)
    
    @staticmethod
    def change_user_role(id: int, role: str) -> tuple:
        """
        Change le rôle d'un utilisateur
        Arguments:
            id: int 
            | L'identifiant de l'utilisateur
            role: str
            | Le nouveau rôle de l'utilisateur
        Exceptions:
            - UserNotExist: si l'utilisateur n'existe pas
            - RoleNotReferenced: si le rôle n'est pas référencé par le User Manager
        
        renvoie un tuple contenant les informations de l'utilisteur avec le rôle modifié
        """
        assert type(id) == int, "id agument must be int"
        assert type(role) == str, "role agument must be str"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Requête SQL changeant le rôle de l'utilisateur
            cursor.execute(f"UPDATE user SET role = '{role}' WHERE id == {id};")
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            raise RoleNotReferenced(role)
        # Récupére les données de l'utilisateur
        return UserManager.get_user(id)

    @staticmethod
    def delete_user(id: int) -> None:
        """
        Supprime un utilisateur
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        ne renvoie rien
        """
        assert type(id) == int, "id agument must be int"
        if not UserManager.user_exist(id): raise UserNotExist(id)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL effaçant l'entrée de l'utilisateur de la base de données
        cursor.execute(f"DELETE FROM user WHERE id == {id};")
        DATA_BASE.commit() # Met à jour la base de données


    @staticmethod
    def get_role_of(id: int) -> str:
        """
        Donne le rôle d'un utilisteur via son identifiant
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        renvoie un str correspondant au rôle de l'utilisateur
        """
        assert type(id) == int, "id agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le rôle de l'utilisateu
        response = cursor.execute(f"SELECT role FROM user WHERE id == {id};")
        role = response.fetchone() # On récupére les données

        if role is None: raise UserNotExist(id)
        return role[0]

    @staticmethod
    def get_permission_level_of(role: str) -> int:
        """
        Donne le niveau de permision d'un rôle référencé
        Argument:
            role: str
            | Le nouveau rôle de l'utilisateur
        Exception:
            - RoleNotReferenced: si le rôle n'est pas référencé par le User Manager
        
        renvoie le niveau de pemision du rôle (int)
        """
        assert type(role) == str, "role agument must be str"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le niveau de permission du rôle
        response = cursor.execute(f"SELECT level_permission FROM roles_ref WHERE name == '{role}';")
        level_permission = response.fetchone() # On récupére les données
        
        if level_permission is None: raise RoleNotReferenced(role)
        return  level_permission[0]

    @staticmethod
    def get_money_of(id: int) -> int:
        """
        Donne le montant de l'agent d'un utilisateu via son id
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        renvoie le montant de l'argent de l'utilisateur
        """
        assert type(id) == int, "id agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL récupérant le montant de l'agent de l'utilisateur
        response = cursor.execute(f"SELECT money FROM user WHERE id == {id};")
        money = response.fetchone() # On récupére les données

        if money is None: raise UserNotExist(id)
        return money[0]
    
    @staticmethod
    def set_money_of(id: int, money: int) -> int:
        """
        Change le montant de l'agent d'un utilisateu via son id
        Arguments:
            id: int 
            | L'identifiant de l'utilisateur
            money: int
            | Le montant de l'argent à définir
        Exception:
            - UserNotExist: si l'utilisateur n'existe pas
        
        ne renvoie rien
        """
        assert type(id) == int, "id agument must be int"
        if not UserManager.user_exist(id): raise UserNotExist(id)
        assert type(money) == int, "money agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL changent le montant de l'agent de l'utilisateur
        cursor.execute(f"UPDATE user SET money = {money} WHERE id == {id};")
        DATA_BASE.commit() # Met à jour la base de données