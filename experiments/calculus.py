from math import log


class Calculus:

    @staticmethod
    def value(msg):
        return sum([round(log(len(i))/10, 2) for i in msg.split(' ')])
