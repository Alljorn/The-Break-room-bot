from game.supplies.supply import Suplly
from game.effects.effect import Effect


class Drink(Suplly):

    def __init__(self, name: str, effect: Effect) -> None:
        super().__init__(name)
        self.__effect = effect

    def __repr__(self) -> str:
        return f"{self.get_name()}: {self.__effect} effect"