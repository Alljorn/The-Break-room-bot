from game.distributor import Distributor

from game.supplies.foods.apple import Apple
from game.supplies.foods.chocolate_bar import ChocolateBar

from game.supplies.drinks.cola import Cola
from game.supplies.drinks.orange_juice import OrangeJuice



supply_type_ref = [
    Apple,ChocolateBar,Cola,OrangeJuice
]
distributor = Distributor()




if __name__ == '__main__':
    

    distributor.supply(Apple("Golden Apple"), 3)
    distributor.supply(Apple("Golden Apple"), 3)
    distributor.supply(Apple("Red Apple"), 3)
    distributor.supply(Cola("Chery Cola"), 1)

    print(distributor)
    length_at_3 = distributor.get_length_at(3)
    print("Length at 3:", length_at_3, f"suppl{'y' if length_at_3 <= 1 else 'ies'}")
    