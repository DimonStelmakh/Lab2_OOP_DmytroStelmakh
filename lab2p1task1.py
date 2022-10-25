class Ticket:
    def __init__(self, number, price, regular_price, ticket_type):
        self.number = number
        self.price = price
        self.regular_price = regular_price
        self.ticket_type = ticket_type

    @property
    def number(self):
        return self.__number

    @property
    def price(self):
        return int(self.__price)

    @property
    def regular_price(self):
        return int(self.__regular_price)

    @property
    def ticket_type(self):
        return self.__ticket_type

    @number.setter
    def number(self, value):
        if isinstance(value, int):
            self.__number = value
        else:
            raise TypeError('TypeError. Expected "int" type')

    @price.setter
    def price(self, value):
        if isinstance(value, (int, float)):
            self.__price = value
        else:
            raise TypeError('TypeError. Expected "int" or "float" type')

    @regular_price.setter
    def regular_price(self, value):
        if isinstance(value, (int, float)):
            self.__regular_price = value
        else:
            raise TypeError('TypeError. Expected "int" or "float" type')

    @ticket_type.setter
    def ticket_type(self, value):
        if isinstance(value, str):
            self.__ticket_type = value
        else:
            raise TypeError('TypeError. Expected "str" type')

    def __str__(self):
        return f'Number: {self.__number}, price: {int(self.__price)}, type: {self.__ticket_type}'


class RegularTicket(Ticket):
    def __init__(self, number, regular_price=100):
        super().__init__(number, regular_price, regular_price, 'Regular')


class AdvanceTicket(Ticket):
    def __init__(self, number, regular_price=100):
        super().__init__(number, regular_price/10*6, regular_price, 'Advance')


class StudentTicket(Ticket):
    def __init__(self, number, regular_price=100):
        super().__init__(number, regular_price/10*5, regular_price, 'Student')


class LateTicket(Ticket):
    def __init__(self, number, regular_price=100):
        super().__init__(number, regular_price/10*11, regular_price, 'Late')


def main():
    rg = RegularTicket(18956, 100)
    print(rg)
    ad = AdvanceTicket(12389, 100)
    print(ad)
    st = StudentTicket(14634)  # default parameter (100) used here
    print(st)
    lt = LateTicket(48245)  # default parameter (100) used here
    print(lt)
    print("The real price of this late ticket is:", lt.price)
    print("The regular price based on which the real one was made is:", lt.regular_price)


main()
