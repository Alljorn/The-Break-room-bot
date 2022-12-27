
class DataTable:
    """
    class DataBase(*, primary_key=None)
    Attributs:              Méthodes:
    | name                  | get_name
    | template              | get_template
    | primary_key           | get_primary_key


    Une base de donnée, modifiable et enregistrable.
    Il est possible de définir une clé primaire permettant d'assurer l'unité des données.

        | propriété name
            type: str
            Le nom de la table de donnée.

        | propriété template
            type: dict
            Le template est le model des données de la table, il indique le nom des attributs de la table et leur type
            sous la forme: {"attribut1": type1, "attribut2": type2, ...}

        | propriété primary_key
            type: optionel[any]
            La clé primaire assure l'unité de chaque entrée de la table, les valeurs de l'attribut qu'elle cible doivent
            être unique.

        | propriété data
            type: dict | list
            Les données de la table, chaque entrée y est enregistrée.
    
        -

        | get_name()
        return: str
        Renvoie le nom de la table.

        | get_template()
        return: dict
        Renvoie le template de la table.

        | get_primary_key()
        return: any
        Renvoie la clé primaire de la table, None si non définie.

        | get()
        return: dict | list
        Renvoie les données de la table.

        | have_primary_key()
        return: bool
        Renvoie True si le table a une clé primaire, False sinon.

        | is_empty()
        return: bool
        Renvoie True si la table est vide, False sinon.

        | insert(entry)
        return: None
        Argument:
            | entry
                type: dict
                L'entrée à inserer sous la forme du template.
        Insert une entrée dans la table, ne renvoie rien.

        | remove_in(attribute, value)
        return: None
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à supprimer
            | value
                type: any
                La valeur à supprimer
        Supprime toute les occurences de 'value' dans l'attribut 'attibute' de chaque entrée de la table.

        | select(attribute, value)
        return: list[dict]
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à rechercher
            | value
                type: any
                La valeur à rechercher
        Renvoie toute les entrées où 'value' de l'attribut 'attribute' est présent.

        | edit(attribute, value, new_value)
        return: None
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à modifier
            | value
                type: any
                La valeur à modifier
            | new_value
                type: any
                La nouvelle valeur
        Modifie toute les occurences de 'value' dans l'attribut 'attibute' de chaque entrée de la table.
    """

    def __init__(self, name: str, template: dict, primary_key: any = None) -> None:
        assert type(name) == str, "name argument must be str"
        assert type(template) == dict, "template argument must be dict"
        if primary_key is not None: assert primary_key in template, "primary key must be in template"

        self.__PRIMARY_KEY = primary_key
        self.__TEMPLATE = template
        self.__NAME = name
        self.__data = {} if primary_key is not None else []

    def get_name(self) -> str:
        """
        return: str
        Renvoie le nom de la table.
        """
        return self.__NAME

    def get_template(self) -> dict:
        """
        return: dict
        Renvoie le template de la table.
        """
        return dict(self.__TEMPLATE)

    def get_primary_key(self) -> any:
        """
        return: any
        Renvoie la clé primaire de la table, None si non définie.
        """
        return self.__PRIMARY_KEY

    def get(self) -> dict | list:
        """
        return: dict | list
        Renvoie les données de la table.
        """
        return self.__data
    

    def have_primary_key(self) -> bool:
        """
        return: bool
        Renvoie True si le table a une clé primaire, False sinon.
        """
        return self.__PRIMARY_KEY is not None
    
    def is_empty(self) -> bool:
        """
        return: bool
        Renvoie True si la table est vide, False sinon.
        """
        if self.have_primary_key():
            return self.__data == {}
        else:
            return self.__data == []

    
    def insert(self, entry: dict) -> None:
        """
        return: None
        Argument:
            | entry
                type: dict
                L'entrée à inserer sous la forme du template.
        Insert une entrée dans la table, ne renvoie rien.
        """
        for attribute in entry:
            assert attribute in self.__TEMPLATE, f"{attribute} not in template"
            assert type(entry[attribute]) == self.__TEMPLATE[attribute], f"{type(entry[attribute]).__name__} type is not {self.__TEMPLATE[attribute].__name__}"
        if self.have_primary_key() and self.__data != {}:
            assert entry[self.__PRIMARY_KEY] not in self.__data, f"{entry[self.__PRIMARY_KEY]} already exist as primary key"

        if self.have_primary_key():
            self.__data[entry[self.__PRIMARY_KEY]] = entry
        else:
            self.__data.append(entry)
    
    def remove_in(self, attribute: any, value: any) -> None:
        """
        return: None
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à supprimer
            | value
                type: any
                La valeur à supprimer
        Supprime toute les occurences de 'value' dans l'attribut 'attibute' de chaque entrée de la table.
        """
        assert attribute in self.__TEMPLATE, f"{attribute} not in template"
        assert type(value) == self.__TEMPLATE[attribute], f"{type(value).__name__} type is not {self.__TEMPLATE[attribute].__name__}"

        if self.have_primary_key():
            if attribute == self.__PRIMARY_KEY:
                if value in self.__data:
                    del self.__data[value]
            else:
                key_to_remove = []
                for key in self.__data:
                    if value == self.__data[key][attribute]:
                        key_to_remove.append(key)
                for key in key_to_remove:
                    del self.__data[key]
        else:
            index_to_remove = []
            for i in range(len(self.__data)):
                if value == self.__data[i][attribute]:
                    index_to_remove.append(i)
            for i in range(len(index_to_remove)):
                del self.__data[index_to_remove[i] - i]

    def select(self, attribute: any, value: any) -> list[dict]:
        """
        return: list[dict]
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à rechercher
            | value
                type: any
                La valeur à rechercher
        Renvoie toute les entrées où 'value' de l'attribut 'attribute' est présent.
        """
        assert attribute in self.__TEMPLATE, f"{attribute} not in template"
        assert type(value) == self.__TEMPLATE[attribute], f"{type(value).__name__} type is not {self.__TEMPLATE[attribute].__name__}"

        entries_to_return = []
        if self.have_primary_key():
            if attribute == self.__PRIMARY_KEY:
                if value in self.__data:
                    entries_to_return.append(self.__data[value])
            else:
                for key in self.__data:
                    if value == self.__data[key][attribute]:
                        entries_to_return.append(self.__data[key])
        else:
            for entry in self.__data:
                if value == entry[attribute]:
                    entries_to_return.append(entry)
        return entries_to_return

    def edit(self, attribute: any, value: any, new_value: any) -> None:
        """
        return: None
        Arguments:
            | attribute
                type: any
                L'attribut de la table où ce situe la valeur à modifier
            | value
                type: any
                La valeur à modifier
            | new_value
                type: any
                La nouvelle valeur
        Modifie toute les occurences de 'value' dans l'attribut 'attibute' de chaque entrée de la table.
        """
        assert attribute in self.__TEMPLATE, f"{attribute} not in template"
        assert type(value) == self.__TEMPLATE[attribute], f"{type(value).__name__} type is not {self.__TEMPLATE[attribute].__name__}"
        assert type(new_value) == self.__TEMPLATE[attribute], f"{type(value).__name__} type is not {self.__TEMPLATE[attribute].__name__}"

        entries = self.select(attribute, value)
        for entry in entries:
            entry[attribute] = new_value


    def __repr__(self) -> str:
        return str(self.__data)


if __name__ == '__main__':

    data = DataTable("user", {"id":int, "role":str}, primary_key="id")
    data.insert( {"id":0, "role":"admin"} )
    data.insert( {"id":1, "role":"classic"} )
    data.insert( {"id":2, "role":"admin2"} )
    print(data)
    print("select >", data.select("id", 2))
    print(data.get())