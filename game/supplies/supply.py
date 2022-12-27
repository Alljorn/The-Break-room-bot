
class Supply:

    repertoire = []
    def add_repertoire(self):
        if not (type(self).__name__,self.get_name()) in Supply.repertoire:
            Supply.repertoire.append( (type(self).__name__,self.get_name()) )
        print(Supply.repertoire)


    def __init__(self, name: str) -> None:
        assert type(name) == str, "name argument must be str"
        self.__name = name
        self.add_repertoire()

    
    def get_name(self) -> str:
        return self.__name

    
    def __repr__(self) -> str:
        return self.__name