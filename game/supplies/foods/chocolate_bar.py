from game.supplies.foods.food import Food


class ChocolateBar(Food):

    def __init__(self, name: str) -> None:
        super().__init__(name, 10)