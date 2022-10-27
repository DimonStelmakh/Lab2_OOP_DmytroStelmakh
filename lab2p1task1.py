import random
from datetime import datetime

# total_value = 0
tickets = []
ans_variants = {'yes', 'yeah', 'y', 'Yes', 'Yeah', 'Y', 'Так', 'так', 'Да', 'да', 'д', 'т', 'Д', 'Т', '+', 'угу', 'ага'}


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
    def __init__(self, number, regular_price, date_of_event):
        super().__init__(number, regular_price * 0.6, regular_price, date_of_event, 'Advance')


class StudentTicket(Ticket):
    def __init__(self, number, regular_price, date_of_event, days_left):
        if days_left > 60:
            super().__init__(number, regular_price * 0.6 * 0.5, regular_price, date_of_event, 'StudentAdvanced')
        elif 0 <= days_left < 10:
            super().__init__(number, regular_price * 1.1 * 0.5, regular_price, date_of_event, 'StudentLate')
        else:
            super().__init__(number, regular_price * 0.5, regular_price, date_of_event, 'Student')


class LateTicket(Ticket):
    def __init__(self, number, regular_price, date_of_event):
        super().__init__(number, regular_price * 1.1, regular_price, date_of_event, 'Late')


def ticket_interpreter(number, regular_price, date_of_event, isstudent):
    if isstudent:
        tickets.append(StudentTicket(number, regular_price, date_of_event))
        print('\n\033[92mA student ticket has been added successfully!\033[0m')
    else:
        days_left = (datetime.strptime(date_of_event, "%Y/%m/%d").date() - datetime.today().date()).days
        if days_left > 60:
            tickets.append(AdvanceTicket(number, regular_price, date_of_event))
            print('\n\033[92mAn advance ticket has been added successfully!\033[0m')
        elif 0 <= days_left < 10:
            tickets.append(LateTicket(number, regular_price, date_of_event))
            print('\n\033[92mA late ticket has been added successfully!\033[0m')
        elif 10 <= days_left <= 60:
            tickets.append(RegularTicket(number, regular_price, date_of_event))
            print('\n\033[92mA regular ticket has been added successfully!\033[0m')
        else:
            raise ValueError('This event has already took place')


def answer_interpreter(answer):
    if answer in ans_variants:
        return True
    else:
        return False


def validate_date_format(date_string):
    try:
        datetime.strptime(date_string, '%Y/%m/%d')
        return True
    except ValueError:
        print(f"\033[91mIncorrect data format, should be yyyy/mm/dd!\033[0m")


def main():
    continuation = True
    valid_date = False
    date_of_event = '2000/01/01'

    while continuation:
        while not valid_date:
            date_of_event = input('Enter a date of the event you want to visit in format yyyy/mm/dd: ')
            valid_date = validate_date_format(date_of_event)

        isstudent = answer_interpreter(input('Are you a student? (+/-): '))

        ticket_interpreter(random.randint(1000, 9999), 100, date_of_event, isstudent)

        print('\nYour tickets:')
        print(*tickets, sep='\n')

        continuation_answer = input('\nWant to buy one more ticket? (+/-): ')
        if not answer_interpreter(continuation_answer):
            continuation = False


main()
