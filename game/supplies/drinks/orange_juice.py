from game.supplies.drinks.drink import Drink
from game.effects.effect import Effect


class OrangeJuice(Drink):

    def __init__(self, name: str) -> None:
        super().__init__(name, Effect())