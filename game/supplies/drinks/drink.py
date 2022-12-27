from game.supplies.supply import Supply
from game.effects.effect import Effect


class Drink(Supply):

    def __init__(self, name: str, effect: Effect) -> None:
        assert type(effect) == Effect, "effect argument must be Effect"
        super().__init__(name)
        self.__effect = effect

    def __repr__(self) -> str:
        return f"{self.get_name()}: {self.__effect} effect"