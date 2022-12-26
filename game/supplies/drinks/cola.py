from game.supplies.drinks.drink import Drink
from game.effects.effect import Effect


class Cola(Drink):

    def __init__(self) -> None:
        super().__init__("Cola", Effect())