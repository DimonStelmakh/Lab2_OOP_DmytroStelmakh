from math import gcd, lcm


class Rational:
    def __init__(self, n=1, d=1):
        self.numerator = n
        self.denominator = d

    def general(self):
        value_of_gcd = gcd(self.numerator, self.denominator)
        return f"{self.numerator // value_of_gcd}/{self.denominator // value_of_gcd}"
        # оператор "//" використовується лише для того, щоб вивести числа як int, а не float

    def floating_point(self):
        return self.numerator / self.denominator

    @property
    def numerator(self):
        return self.__numerator

    @property
    def denominator(self):
        return self.__denominator

    @numerator.setter
    def numerator(self, value):
        if not isinstance(value, int):
            raise TypeError
        self.__numerator = value

    @denominator.setter
    def denominator(self, value):
        if not isinstance(value, int):
            raise TypeError
        if not value:
            raise ZeroDivisionError
        self.__denominator = value

    def __str__(self):
        return f'{self.__numerator}/{self.__denominator}'

    def __add__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            value_of_lcm = lcm(self.denominator, other.denominator)
            num1 = self.numerator * (value_of_lcm // self.denominator)
            num2 = other.numerator * (value_of_lcm // other.denominator)
            ob = Rational(num1+num2, value_of_lcm)
            return ob.general()
        elif isinstance(other, int):
            num = self.numerator + other * self.denominator
            ob = Rational(num, self.denominator)
            return ob.general()
        elif isinstance(other, float):
            return self.floating_point() + other
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            value_of_lcm = lcm(self.denominator, other.denominator)
            num1 = self.numerator * (value_of_lcm // self.denominator)
            num2 = other.numerator * (value_of_lcm // other.denominator)
            ob = Rational(num1-num2, value_of_lcm)
            return ob.general()
        elif isinstance(other, int):
            num = self.numerator - other * self.denominator
            ob = Rational(num, self.denominator)
            return ob.general()
        elif isinstance(other, float):
            return self.floating_point() - other
        else:
            return NotImplemented

    def __rsub__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            value_of_lcm = lcm(self.denominator, other.denominator)
            num1 = self.numerator * (value_of_lcm // self.denominator)
            num2 = other.numerator * (value_of_lcm // other.denominator)
            return Rational(num2-num1, value_of_lcm).general()
        elif isinstance(other, int):
            num = other * self.denominator - self.numerator
            return Rational(num, self.denominator).general()
        elif isinstance(other, float):
            return other - self.floating_point()
        else:
            return NotImplemented

    def __mul__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            return Rational(self.numerator * other.numerator, self.denominator * other.denominator).general()
        elif isinstance(other, int):
            return Rational(self.numerator * other, self.denominator).general()
        elif isinstance(other, float):
            return self.floating_point() * other
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            return Rational(self.numerator * other.denominator, self.denominator * other.numerator).general()
        elif isinstance(other, int):
            return Rational(self.numerator, self.denominator * other).general()
        elif isinstance(other, float):
            return self.floating_point() / other
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if not isinstance(other, (Rational, int, float)):
            return '\033[93mA number expected!\033[0m'
        if isinstance(other, Rational):
            return Rational(other.numerator * self.denominator, other.denominator * self.numerator).general()
        elif isinstance(other, int):
            return Rational(self.denominator * other, self.numerator).general()
        elif isinstance(other, float):
            return other / self.floating_point()
        else:
            return NotImplemented

def main():
    ob1 = Rational(1, 3)
    print('Given numbers for object 1 are', ob1.numerator, 'and', ob1.denominator)

    ob2 = Rational(2, 4)
    print('Given numbers for object 2 are', ob2.numerator, 'and', ob2.denominator)

    print('\nSecond fraction is:')
    print("The general form is:", ob2.general())
    print("The floating point form is:", ob2.floating_point())

    ob2.numerator = 2
    ob2.denominator = 8
    print("The new value for object have been given successfully. They are:", ob2.numerator, 'and', ob2.denominator)

    print('\nNow the second fraction is:')
    print("The general form is:", ob2.general())
    print("The floating point form is:", ob2.floating_point())

    ob3 = Rational()
    print('\nFraction 3 has no provided values during an initialization, so the default parameters are used')
    print('The third fraction is:')
    print("The general form is:", ob3.general())
    print("The floating point form is:", ob3.floating_point())

    print('\n', sep='')
    print(ob1 + ob3, ob1 + 3, ob1 + 0.6666, ob1 + 'f', ob3 + ob1, 3 + ob1, 0.6666 + ob1, sep=', ')
    print(ob1 - ob3, ob1 - 3, ob1 - 0.6666, ob1 - 'f', ob3 - ob1, 3 - ob1, 0.6666 - ob1, sep=', ')
    print(ob1 * ob3, ob1 * 3, ob1 * 0.6666, ob1 * 'f', ob3 * ob1, 3 * ob1, 0.6666 * ob1, sep=', ')
    print(ob1 / ob3, ob1 / 3, ob1 / 0.6666, ob1 / 'f', ob3 / ob1, 3 / ob1, 0.6666 / ob1, sep=', ')


main()
