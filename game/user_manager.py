import sqlite3

from game.data_base import DATA_BASE
from game.exceptions import UserAlreadyExist,UserNotExist,UserRoleNotReferenced

from config.game import DEFAULT_USER_ROLE


class UserManager:
    """
    L'User Manager permet de gérer les données des utilisateur

    Méthodes de classe:
        - change_use_role(id, role): change le rôle d'un utilisateur
        - delete_user(id): supprime un uilisateur
        - get_role_of(id): donne le rôle d'un utilisteur via son identifiant
        - get_roles_ref(): donne les rôles référencés par l'User Manager
        - get_user(id): donne les données d'un utilisateur via son identifiant
        - new_user(id): crée un utilisateur
        - user_exist(id): vérifie qu'un utilisteur existe via son identifiant
    """

    def __init_roles_ref():
        """
        Initialise les rôles référencés dans la base données

        ne renvoie rien
        """
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # On ajoute les différents rôles référencés
        try: cursor.execute("INSERT INTO roles_ref VALUES('administrator');")
        except sqlite3.IntegrityError: pass    
        try: cursor.execute("INSERT INTO roles_ref VALUES('classic');")
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
        Exception
        
        renvoie un tuple contenant les données de l'utilisateur
        """
        assert type(id) == int, "id agument must be int"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL séléctionant l'entrée dans la base de données de l'utilisateurr
        response = cursor.execute(f"SELECT * FROM user WHERE id == {id}")
        return response.fetchone() # On récupére les données

    
    @staticmethod
    def user_exist(id: int) -> bool:
        """
        Vérifie qu'un utilisteur existe via son identifiant
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        
        renvoie True si l'utilisateur existe, False sinon
        """
        return UserManager.get_user(id) is not None

    @staticmethod
    def new_user(id: int) -> tuple:
        """
        Crée un utilisateur
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
        Exception:
            | UserAreadyExist: si l'utilisateur existe déjà
            | UserRoleNotReferenced: si le rôle pr défaut n'est pas référencé
        
        renvoie un tuple contenant les informations de l'utilisteur créé
        """
        assert type(id) == int, "id agument must be int"
        if UserManager.user_exist(id): raise UserAlreadyExist(id)

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Requête SQL ajoutant l'utilisateur avec les paramètres par défaut
            cursor.execute(f"INSERT INTO user VALUES({id}, '{DEFAULT_USER_ROLE}');")
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            raise UserRoleNotReferenced(DEFAULT_USER_ROLE)
        # Récupére les données de l'utilisateur créé
        return UserManager.get_user(id)
    
    @staticmethod
    def change_user_role(id: int, role: str) -> tuple:
        """
        Change le rôle d'un utilisateur
        Argument:
            id: int 
            | L'identifiant de l'utilisateur
            role: str
            | Le nouveau rôle de l'utilisateur
        Exception:
            - UserRoleNotReferenced: si le rôle n'est pas référencé par le User Manager
        
        renvoie un tuple contenant les informations de l'utilisteur avec le rôle modifié
        renvoie None si l'utilisteur n'existe pas
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
            raise UserRoleNotReferenced(role)
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
            | UserNotExist: si l'utilisateur n'existe pas
        
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

        renvoie un str correspondant au rôle de l'utilisateur
        """
        assert type(id) == int, "id agument must be int"
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL effaçant l'entrée de l'utilisateur de la base de données
        response = cursor.execute(f"SELECT role FROM user WHERE id == {id};")
        return response.fetchone() # On récupére les données
