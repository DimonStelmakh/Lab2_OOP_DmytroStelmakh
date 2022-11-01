import random
from datetime import datetime

tickets = []


class Ticket:
    def __init__(self, number, price, regular_price, date_of_event, ticket_type):
        self.number = number
        self.price = price
        self.regular_price = regular_price
        self.ticket_type = ticket_type
        self.__date_of_event = date_of_event
        self.__date_of_purchase = datetime.today()

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
        if not isinstance(value, int):
            raise TypeError('TypeError. Expected "int" type')
        self.__number = value

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('TypeError. Expected "int" or "float" type')
        self.__price = value

    @regular_price.setter
    def regular_price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('TypeError. Expected "int" or "float" type')
        self.__regular_price = value

    @ticket_type.setter
    def ticket_type(self, value):
        if not isinstance(value, str):
            raise TypeError('TypeError. Expected "str" type')
        self.__ticket_type = value

    def __str__(self):
        return f'Number: {self.__number}, price: {int(self.__price)} (regular: {int(self.__regular_price)}), \
date: {self.__date_of_event}, type: {self.__ticket_type}'


class RegularTicket(Ticket):
    def __init__(self, number, regular_price, date_of_event):
        super().__init__(number, regular_price, regular_price, date_of_event, 'Regular')


class AdvanceTicket(Ticket):
    def __init__(self, number, price, regular_price, date_of_event, ticket_type):
        super().__init__(number, price * 0.6, regular_price, date_of_event, ticket_type)


class LateTicket(Ticket):
    def __init__(self, number, price, regular_price, date_of_event, ticket_type):
        super().__init__(number, price * 1.1, regular_price, date_of_event, ticket_type)


class StudentTicket(Ticket):
    def __init__(self, number, regular_price, date_of_event, ticket_type):
        super().__init__(number, regular_price * 0.5, regular_price, date_of_event, ticket_type)


class StudentLateTicket(StudentTicket, LateTicket):
    def __init__(self, number, regular_price, date_of_event):
        super().__init__(number, regular_price, date_of_event, 'Student Late')


class StudentAdvanceTicket(StudentTicket, AdvanceTicket):
    def __init__(self, number, regular_price, date_of_event):
        super().__init__(number, regular_price, date_of_event, 'Student Advance')


def ticket_interpreter(number, regular_price, date_of_event, isstudent, day_late=10):
    days_left = (datetime.strptime(date_of_event, "%Y/%m/%d").date() - datetime.today().date()).days
    if days_left < 0:
        return '\033[93m''This event has already taken place\033[0m'
    if isstudent:
        if days_left > 60:
            tickets.append(StudentAdvanceTicket(number, regular_price, date_of_event))
            return '\033[92mA student advance ticket has been added successfully!\033[0m'
        elif 0 <= days_left < 10:
            tickets.append(StudentLateTicket(number, regular_price, date_of_event))
            return '\033[92mA student late ticket has been added successfully!\033[0m'
        else:
            tickets.append(StudentTicket(number, regular_price, date_of_event, 'Student'))
            return '\033[92mA student ticket has been added successfully!\033[0m'
    else:
        if days_left > 60:
            tickets.append(AdvanceTicket(number, regular_price, regular_price, date_of_event, 'Advance'))
            return '\033[92mAn advance ticket has been added successfully!\033[0m'
        elif 0 <= days_left < 10:
            tickets.append(LateTicket(number, regular_price, regular_price, date_of_event, 'Late'))
            return '\033[92mA late ticket has been added successfully!\033[0m'
        else:
            tickets.append(RegularTicket(number, regular_price, date_of_event))
            return '\033[92mA regular ticket has been added successfully!\033[0m'


def answer_interpreter(answer):
    return True if answer in ('yes', 'yeah', 'y', 'Yes', 'Yeah', 'Y', 'Так', 'так', 'Да', 'да', 'д', 'т', 'Д', 'Т', '+',
                              'угу', 'ага') else False


def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y/%m/%d')
    except ValueError:
        print("\033[91mIncorrect date format (should be yyyy/mm/dd) or this date doesn't exist!\033[0m")
        return False
    else:
        return True


def ticket_finder(key):
    try:
        return [ele for ele in tickets if ele.number == key].pop()
    except IndexError:
        return '\033[93mThere is no such ticket!\033[0m'
    except ValueError:
        return '\033[91mEnter a number in an appropriate format: 4 numerals\033[0m'


def main():
    date_of_event = '2000/01/01'  # на випадок проблем з інпутом

    continuation = True
    while continuation:
        valid_date = False
        while not valid_date:
            date_of_event = input('Enter a date of the event you want to visit in format yyyy/mm/dd: ')
            valid_date = validate_date_format(date_of_event)

        isstudent = answer_interpreter(input('Are you a student? (+/-): '))

        print(ticket_interpreter(random.randint(1000, 9999), 100, date_of_event, isstudent))

        print('\nYour tickets:', *tickets, sep='\n')

        continuation = answer_interpreter(input('\nWant to buy one more ticket? (+/-): '))

    find_answer = answer_interpreter(input('Want to find a ticket among those you have bought? (+/-): '))

    continuation = True
    while continuation:
        if find_answer:
            print(ticket_finder(int(input('\nEnter a ticket number: '))))
            continuation = answer_interpreter(input('\nWant to find another one? (+/-): '))


main()
