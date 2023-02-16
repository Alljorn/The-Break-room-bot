import math


class Calculus:

    @staticmethod
    def value(msg: list) -> float:
        return round(math.fsum([math.log(len(i))/60
                                for i in msg.split(' ')]), 2)
