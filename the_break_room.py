

if __name__ == '__main__':
    from game.distributor import Distributor
    from game.supplies.foods.apple import Apple
    from game.supplies.drinks.cola import Cola

    distr = Distributor()
    distr.supply(Apple(), 3)
    distr.supply(Apple(), 3)
    distr.supply(Cola(), 1)

    print(distr)
    length_at_3 = distr.get_length_at(3)
    length_at_3 = 1
    print("Length at 3:", length_at_3, f"suppl{'y' if length_at_3 <= 1 else 'ies'}")
    