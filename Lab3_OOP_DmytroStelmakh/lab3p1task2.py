class Composition:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    @property
    def name(self):
        return self.__name

    @property
    def quantity(self):
        return self.__quantity

    @property
    def price(self):
        return self.__price

    @name.setter
    def name(self, value):
        self.__name = value

    @quantity.setter
    def quantity(self, value):
        try:
            value = int(value)
        except ValueError:
            raise TypeError('Quantity should be a number')
        if value <= 0:
            raise ValueError('Quantity should more than 0')

        self.__quantity = value

    @price.setter
    def price(self, value):
        try:
            value = round(float(value), 2)
        except ValueError:
            raise TypeError('Price should be a numeber')
        if value <= 0:
            raise ValueError('Price should be more than 0')

        self.__price = value

    def __gt__(self, other):
        if isinstance(other, Composition):
            return self.price > other.price
        elif isinstance(other, int):
            return self.price > other
        elif isinstance(other, float):
            return self.price > round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __lt__(self, other):
        if isinstance(other, Composition):
            return self.price < other.price
        elif isinstance(other, int):
            return self.price < other
        elif isinstance(other, float):
            return self.price < round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __ge__(self, other):
        if isinstance(other, Composition):
            return self.price >= other.price
        elif isinstance(other, int):
            return self.price >= other
        elif isinstance(other, float):
            return self.price >= round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __le__(self, other):
        if isinstance(other, Composition):
            return self.price <= other.price
        elif isinstance(other, int):
            return self.price <= other
        elif isinstance(other, float):
            return self.price <= round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __eq__(self, other):
        if isinstance(other, Composition):
            return self.price == other.price
        elif isinstance(other, int):
            return self.price == other
        elif isinstance(other, float):
            return self.price == round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __ne__(self, other):
        if isinstance(other, Composition):
            return self.price != other.price
        elif isinstance(other, int):
            return self.price != other
        elif isinstance(other, float):
            return self.price != round(other, 2)
        else:
            raise TypeError('Can\'t compare a "Composition" with not "Composition" or not number')

    def __add__(self, other):
        if other.isdigit():
            self.__quantity += int(other)

    def __sub__(self, other):
        if other.isdigit():
            self.__quantity -= int(other)

    def __str__(self):
        return f'Good: {self.__name}    Quanity: {self.__quantity}    Price for 1 unit: {self.__price}'


class Request:
    def __init__(self):
        self.names = []
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.names):
            self.index += 1
            return self.names[self.index - 1]
        raise StopIteration

    def __add__(self, other):
        if isinstance(other, str):
            self.names.append(other)
        elif isinstance(other, Request):
            for good in other:
                self.names.append(good)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)


def report(stock, request):
    if not isinstance(stock, (list, tuple, dict)):
        raise TypeError('The first parameter "stock" should be an iterable sequence')
    if not isinstance(request, Request):
        raise TypeError('The second parameter "request" should be an instance of class "Request"')




def main():
    stock = Composition()
    print(stock)


main()
