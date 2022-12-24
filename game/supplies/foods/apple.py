from game.supplies.foods.food import Food


class Apple(Food):

    def __init__(self) -> None:
        super().__init__("Pomme", 15)