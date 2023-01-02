import sqlite3

from game.data.data_base import DATA_BASE
from game.exceptions import SupplyAlreadyExist, SupplyNotExist, TypeNotReferenced, EffectNotExist


class SupplyManager:
    """
    Le Supply Manager permet de gérer les données des produits

    Méthodes de classes:
        - delete_supply(name): supprime un produit
        - get_supplies_types_ref(): donne les types de produits référencés par le Supply Manager
        - get_supply(name): donne les données d'un produit via son nom
        - new_supply(name, type_name, effect_name="NULL"): crée un nouveau produit
        - supply_exist(name): vérifie qu'un produit existe via son nom
        - supply_type_exist(type_name): vérifie qu'un type soit référencé par le Supply Manager
    """

    @staticmethod
    def get_supplies_types_ref() -> list[tuple]:
        """
        Donne les types de produits référencés par le Supply Manager
        
        renvoie une liste de tuple contenant les types de produits référencés par le Supply Manager
        """
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL qui récupére le nom de tout les types référencés
        response = cursor.execute("""
                                  SELECT name
                                  FROM supplies_types_ref;
                                  """)
        return response.fetchall() # On récupère les données

    @staticmethod
    def supply_type_exist(type_name: str) -> bool:
        """
        Vérifie qu'un type soit référencé par le Supply Manager
        Argument:
            type_name: str
            | Le type à vérifier

        renvoie True si le type est référencé, False sinon
        """
        assert type(type_name) == str, "type_name agument must be str"

        for type_ref in SupplyManager.get_supplies_types_ref():
            if type_name in type_ref: return True
        return False
    
    @staticmethod
    def get_supply(name: str) -> tuple:
        """
        Donne les données d'un produit via son nom
        Argument:
            name: str
            | Le nom du produit
        Exception:
            - SupplyNotExist: si le produit n'existe pas

        renvoie un tuple contenant les données du produit
        """
        assert type(name) == str, "name agument must be str"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL séléctionant l'entrée dans la base de données du produit
        response = cursor.execute(f"""
                                   SELECT *
                                   FROM supply
                                   WHERE name == '{name}';
                                   """)
        supply_data = response.fetchone() # On récupére les données

        if supply_data is None: raise SupplyNotExist(name)
        return supply_data

    @staticmethod
    def supply_exist(name: str) -> bool:
        """
        Vérifie qu'un produit existe via son nom
        Argument:
            name: str
            | Le nom du produit
        
        renvoie True si le produit existe, False sinon
        """
        assert type(name) == str, "name agument must be str"
        
        try:
            SupplyManager.get_supply(name)
            return True
        except SupplyNotExist:
            return False

    @staticmethod
    def new_supply(name: str, type_name: str, effect_name: str = "NULL") -> None:
        """
        Crée un nouveau produit
        Arguments:
            name: str
            | Le nom du produit
            type_name: str
            | Le type du produit
            effect_name: str
            | Le nom de l'effet du produit
        Exceptions:
            - SupplyAlreadyExist: si le produit existe déjà
            - TypeNotReferenced: si le type n'est pas référencé par le Supply Manager
            - EffectNotExist: si l'effet n'existe pas
        
        ne renvoie rien
        """
        assert type(name) == str, "name agument must be str"
        if SupplyManager.supply_exist(name): raise SupplyAlreadyExist(name)
        assert type(type_name) == str, "type_name agument must be str"
        assert type(effect_name) == str, "effect_name agument must be str"

        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        try:
            # Gére le cas du NULL effect
            if effect_name != "NULL": effect_name = "'" + effect_name + "'"
            # Requête SQL ajoutant le produit à la base de données
            cursor.execute(f"""
                            INSERT INTO supply
                            VALUES('{name}', '{type_name}', {effect_name});
                            """)
            DATA_BASE.commit() # Met à jour la base de données
        except sqlite3.IntegrityError:
            if not SupplyManager.supply_type_exist(type_name): raise TypeNotReferenced(type_name)
            else: raise EffectNotExist(effect_name)
    
    @staticmethod
    def delete_supply(name: str) -> None:
        """
        Supprime un produit
        Argument:
            name: str
            | Le nom du produit
        Exception:
            - SupplyNotExist: si le produit n'existe pas
        
        ne renvoie rien
        """
        assert type(name) == str, "name agument must be str"
        if not SupplyManager.supply_exist(name): raise SupplyNotExist(name)
        
        # On récupére le curseur SQL pour executer une requête
        cursor = DATA_BASE.cursor()
        # Requête SQL effaçant l'entrée du produit de la base de données
        cursor.execute(f"""
                        DELETE FROM supply
                        WHERE name == '{name}';
                        """)
        DATA_BASE.commit() # Met à jour la base de données