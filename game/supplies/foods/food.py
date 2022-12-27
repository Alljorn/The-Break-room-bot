from game.supplies.supply import Supply


class Food(Supply):

    def __init__(self, name: str, stamina: int) -> None:
        assert type(stamina) == int, "stamina argument must be int"
        super().__init__(name)
        self.__stamina = stamina

    def __repr__(self) -> str:
        return f"{self.get_name()}: {self.__stamina} stamina"
