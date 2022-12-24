from drink import Drink
from game.effects.effect import Effect


class OrangeJuice(Drink):

    def __init__(self) -> None:
        super().__init__("Jus d'orange", Effect())