import random
from datetime import datetime

tickets = []
events = []


class Ticket:
    def __init__(self, number, event, actual_price, ticket_type):
        self.number = number
        self.actual_price = actual_price
        self.event = event
        self.ticket_type = ticket_type
        self.__date_of_purchase = datetime.today()

    @property
    def number(self):
        return self.__number

    @property
    def actual_price(self):
        return int(self.__actual_price)

    @property
    def event(self):
        return self.event

    @property
    def ticket_type(self):
        return self.__ticket_type

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('TypeError. Expected "int" type')
        self.__number = value

    @actual_price.setter
    def actual_price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('TypeError. Expected "int" or "float" type')
        self.__actual_price = value

    @event.setter
    def event(self, value):
        if not isinstance(value, Event):
            raise TypeError('TypeError. Expected "Event" type')
        self.__event = value

    @ticket_type.setter
    def ticket_type(self, value):
        if not isinstance(value, str):
            raise TypeError('TypeError. Expected "str" type')
        self.__ticket_type = value

    def __str__(self):
        return f'Number: {self.__number}, event: {self.__event.name}, price: {self.__actual_price}' \
               f' (regular: {int(self.__event.regular_price)}), date: {self.__event.date_of_event},' \
               f' type: {self.__ticket_type}'


class RegularTicket(Ticket):
    def __init__(self, number, event):
        super().__init__(number, event, event.regular_price, 'Regular')


class AdvanceTicket(Ticket):
    def __init__(self, number, event, actual_price, ticket_type):
        super().__init__(number, event, actual_price * event.kfs['Advance'], ticket_type)


class LateTicket(Ticket):
    def __init__(self, number, event, actual_price, ticket_type):
        super().__init__(number, event, actual_price * event.kfs['Late'], ticket_type)


class StudentTicket(Ticket):
    def __init__(self, number, event, actual_price, ticket_type):
        super().__init__(number, event, actual_price * event.kfs['Student'], ticket_type)


class StudentLateTicket(StudentTicket, LateTicket):
    def __init__(self, number, event, actual_price):
        super().__init__(number, event, actual_price, 'Student Late')


class StudentAdvanceTicket(StudentTicket, AdvanceTicket):
    def __init__(self, number, event, actual_price):
        super().__init__(number, event, actual_price, 'Student Advance')


class Event:
    def __init__(self, name, date_of_event, regular_price, days_separation_names, days, ticket_types, kfs):

        if len(kfs) is not len(ticket_types) and len(days_separation_names) is not len(days):
            raise AttributeError('\033[91mThe number of tickets in not the same as the number of koefs\
            or the number\nof days separation names in not the same as the number of days listed\033[0m')

        self.name = name
        self.date_of_event = date_of_event
        self.regular_price = regular_price

        if kfs:
            self.kfs = {}
            for i in range(len(kfs)):
                self.kfs[ticket_types[i]] = kfs[i]
        if days:
            self.days = {}
            for i in range(len(days)):
                self.days[days_separation_names[i]] = days[i]

    def __str__(self):
        return f'NAME: {self.__name}, DATE: {self.date_of_event}, PRICE: {self.regular_price} UAH,' \
               f' TICKET TYPES: {list(self.kfs.keys())}'

    @property
    def name(self):
        return self.__name

    @property
    def date_of_event(self):
        return self.__date_of_event

    @property
    def regular_price(self):
        return self.__regular_price

    @name.setter
    def name(self, value):
        self.__name = value

    @date_of_event.setter
    def date_of_event(self, value):
        if validate_date_format(value):
            value = datetime.strptime(value, '%Y/%m/%d').date()
            self.__date_of_event = value
        else:
            raise ValueError('Incorrect date!')

    @regular_price.setter
    def regular_price(self, value):
        try:
            self.__regular_price = int(value)
        except ValueError:
            raise ValueError('Price is not a number!')


def ticket_interpreter(number, event, isstudent):
    actual_price = event.regular_price
    days_left = (event.date_of_event - datetime.today().date()).days

    if days_left < 0:
        return '\033[93m''This event has already taken place!\033[0m'
    if event.kfs['Student'] and isstudent:
        if event.days['Advance'] and days_left > event.days['Advance'] and event.kfs['Advanve']:
            tickets.append(StudentAdvanceTicket(number, event))
            return '\033[92mA student advance ticket has been added successfully!\033[0m'
        elif event.days['Late'] and 0 <= days_left < event.days['Late'] and event.kfs['Late']:
            tickets.append(StudentLateTicket(number, event))
            return '\033[92mA student late ticket has been added successfully!\033[0m'
        else:
            tickets.append(StudentTicket(number, event, 'Student'))
            return '\033[92mA student ticket has been added successfully!\033[0m'
    else:
        if event.days['Advance'] and days_left > event.days['Advance'] and event.kfs['Advance']:
            tickets.append(AdvanceTicket(number, event, 'Advance'))
            return '\033[92mAn advance ticket has been added successfully!\033[0m'
        elif event.days['Late'] and 0 <= days_left < event.days['Late'] and event.kfs['Late']:
            tickets.append(LateTicket(number, event, 'Late'))
            return '\033[92mA late ticket has been added successfully!\033[0m'
        else:
            tickets.append(RegularTicket(number, event, 'Regular'))
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


def add_event():
    date = '2000/01/01'  # на випадок проблем з інпутом

    all_single_ticket_types = ['Student', 'Regular', 'Late', 'Advance']

    name = str(input('Enter a name of the event: '))

    valid_date = False
    while not valid_date:
        date = input('Enter a date of the event in format yyyy/mm/dd: ')
        valid_date = validate_date_format(date)

    price = 100
    success = False
    while not success:
        try:
            price = int(input('Enter a regular price of the event: '))
        except ValueError:
            print('\033[93mEnter a number!\033[0m')
        else:
            if price >= 0:
                success = True
            else:
                print('\033[93mEnter a price which is bigger than 0 or equal to 0!\033[0m')

    ticket_types = []
    kfs = []
    answer = answer_interpreter(input(f'Do you want to add a new ticket type for {name}?: '))
    i = 0
    while answer:

        ticket_type = ''
        success = False
        while not success:
            ticket_type = input('Enter a name of the ticket type: ')
            if ticket_type in all_single_ticket_types:
                ticket_types.insert(i, ticket_type)
                success = True
            else:
                print(f'\033[93mThis type of ticket is unavailable to add!\033[0m\n'
                      f'Here is the list of available tickets:\n{all_single_ticket_types}')

        max_kf = 10

        success = False
        while not success:
            try:
                kf = float(input(f'Enter a coefficient that the regular price is multiplied by for the {ticket_type}'
                                 f' ticket.\nDefault value is 1 (no multiplication): '))
            except ValueError:
                print('\033[93mEnter a number!\033[0m')
            else:
                if 0 <= kf <= max_kf:
                    kfs.insert(i, kf)
                    print(f'\033[92mA ticket type {ticket_type} for event {name} has been added successfully!\033[0m')
                    i += 1
                    success = True
                else:
                    print(f'\033[93mEnter a number between 0 and {max_kf}!\033[0m')

        answer = answer_interpreter(input(f'Do you want to add a new ticket type for {name}?: '))

    days_separation_names = []
    days = []
    answer = answer_interpreter(input(f'Do you want to add a new key number of days for ticket types'
                                      f'separation for {name}?: '))
    i = 0
    while answer:
        days_separation_name = ''
        success = False
        while not success:
            days_separation_name = input('Enter a name of the number of days for separation: ')
            if days_separation_name in all_single_ticket_types:
                days_separation_names.insert(i, days_separation_name)
                success = True
            else:
                print(f'\033[93mThis days of separation number is unavailable to add!\033[0m\n'
                      f'Here is the list of available names for days of separation:\n{all_single_ticket_types}')

        success = False
        while not success:
            try:
                day = int(input(f'Enter a number of days for the {days_separation_name} separation: '))
            except ValueError:
                print('\033[93mEnter a number!\033[0m')
            else:
                if day >= 0:
                    days.insert(i, day)
                    print(f'\033[92mDays of separation for {days_separation_name} ticket for event {name} has been'
                          f' added successfully!\033[0m')
                    i += 1
                    success = True
                else:
                    print(f'\033[93mEnter a number which is bigger than 0 or equal to 0!\033[0m')

        answer = answer_interpreter(input(f'Do you want to add a new key number of days for ticket types'
                                          f' separation for {name}?: '))

    events.append(Event(name, date, price, days_separation_names, days, ticket_types, kfs))
    print(f'\033[92mAn event {name} has been formed successfully!\033[0m')


def event_finder(key, by_date):
    if by_date:
        if validate_date_format(key):
            try:
                key = datetime.strptime(key, '%Y/%m/%d').date()
                return [ele for ele in events if ele.date_of_event == key].pop()
            except IndexError:
                return '\033[93mThere is no such event!\033[0m'
        else:
            return '\033[91mEnter a date in an appropriate format: yyyy/mm/dd !\033[0m'
    else:
        try:
            return [ele for ele in events if ele.date == key].pop()
        except IndexError:
            return '\033[93mThere is no such event!\033[0m'


def main():
    date_of_event = '2023/01/01'

    # ev = Event('Stepan Hiha concert', '2023/02/02', 200, ['Late', 'Advance'], [10, 60], ['Late', 'Advance', 'Student',
    #            [1.1, 0.6, 0.5])

    continuation = answer_interpreter(input('Do you want to add an event?: '))
    while continuation:
        add_event()
        continuation = answer_interpreter(input('Do you want to add an event?: '))

    # print(*events, sep='\n')

    continuation = True
    while continuation:

        search_by_date = answer_interpreter(input('Do you want to find an event to visit by date or by name?\n'
                                                  'If by date, enter "+" or "yes", if by name, enter "-" or "no": '))

        key = '2023/01/01'

        alright = False
        while not alright:
            if search_by_date:
                valid_date = False
                while not valid_date:
                    key = input('Enter a date of the event you want to visit in format yyyy/mm/dd: ')
                    valid_date = validate_date_format(date_of_event)
            else:
                key = input('Enter a name of the event: ')

            event = event_finder(key, search_by_date)

            if isinstance(event, Event):
                print('An event found is: ', event, sep='')
                alright = answer_interpreter(input('\nAlright?'))
            else:
                print(event)

        isstudent = answer_interpreter(input('Are you a student? (+/-): '))

        print(ticket_interpreter(random.randint(1000, 9999), event, isstudent))

        print('\nYour tickets:', *tickets, sep='\n')

        continuation = answer_interpreter(input('\nWant to buy one more ticket? (+/-): '))

    find_answer = answer_interpreter(input('Want to find a ticket among those you have bought? (+/-): '))

    continuation = True
    while continuation:
        if find_answer:
            print(ticket_finder(int(input('\nEnter a ticket number: '))))
            continuation = answer_interpreter(input('\nWant to find another one? (+/-): '))


main()
