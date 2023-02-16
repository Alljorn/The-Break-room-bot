from math import log


class Calculus:

    @staticmethod
    def value(msg):
        return sum([round(log(i)/10, 2) for i in len(msg.split(' '))*0.02])
