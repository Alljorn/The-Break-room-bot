from game.supplies.supply import Suplly


class Distributor:

    def __init__(self) -> None:
        self.__stock = {
            1: {}, 2: {}, 3: {},
            4: {}, 5: {}, 6: {},
            7: {}, 8: {}, 9: {},
                   0: {}
        }


    def supply(self, supply: Suplly, at_num: int) -> None:
        assert isinstance(supply, Suplly), f"supply agument must be Suplly"
        assert type(at_num) == int, f"at_num agument must be int"
        assert 0 <= at_num <= 9, "at_num argument must be between 0 and 10"

        if self.__stock[at_num] == {}:
            self.__stock[at_num] = {'type':type(supply), 'content':[supply]}
        else:
            assert self.__stock[at_num]['type'] == type(supply), "Can't mix two different supply"
            self.__stock[at_num]['content'].append(supply)
    

    def get_length_at(self, num: int) -> int:
        assert type(num) == int, f"at_num agument must be int"
        assert 0 <= num <= 9, "at_num argument must be between 0 and 10"

        if self.__stock[num] == {}:
            return 0
        else:
            return len(self.__stock[num]['content'])

    def get_type_at(self, num: int) -> str:
        assert type(num) == int, f"at_num agument must be int"
        assert 0 <= num <= 9, "at_num argument must be between 0 and 10"

        if self.__stock[num] == {}:
            return "empty"
        else:
            return self.__stock[num]['type'].__name__


    def __repr__(self) -> str:
        affichage = ""
        for i in range(10):
            if self.__stock[i] == {}:
                affichage += f"{i} - empty\n"
            else:
                affichage += f"{i} - {self.__stock[i]['content'][-1]}\n"
        return affichage