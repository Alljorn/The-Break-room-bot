from game.supplies.foods.food import Food


class ChocolateBar(Food):

    def __init__(self) -> None:
        super().__init__("Bar de chocolat", 10)