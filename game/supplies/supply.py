
class Suplly:

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.__name