

class Frac:

    def __init__(self, num, denom):
        self.__num = num
        self.__denom = denom
        if denom == 0:
            raise ZeroDivisionError

    def __repr__(self):
        readable = '{}/{}'.format(self.__num, self.__denom)
        return readable

    def __mul__(self, other):
        new_num = self.__num * other.__num
        new_denom = self.__denom * other.__denom
        return Frac(new_num, new_denom)

    def __add__(self, other):
        new_num = self.__num * other.__denom + other.__num * self.__denom
        new_denom = self.__denom * other.__denom
        return Frac(new_num, new_denom)

    def __float__(self):
        float_number = self.__num / self.__denom
        return float_number

    def __eq__(self, other):
        if self.__num * other.__denom == self.__denom * other.__num:
            self.__num / self.__denom == other.__num / other.__denom is True




