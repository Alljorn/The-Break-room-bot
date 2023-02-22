import math


class Calculus:

    @staticmethod
    def value(msg: list) -> float:
        msg = [i for i in msg.split(' ') if i != '']
        return round(math.fsum([math.log(len(i))/60 for i in msg]), 2)
