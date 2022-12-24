from game.supplies.supply import Suplly


class Food(Suplly):

    def __init__(self, name: str, stamina: int) -> None:
        super().__init__(name)
        self.__stamina = stamina

    def __repr__(self) -> str:
        return f"{self.get_name()}: {self.__stamina} stamina"
