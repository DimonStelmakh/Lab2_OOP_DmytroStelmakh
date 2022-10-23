import re

class Pizza:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError('TypeError. Expected "str" type')

    @size.setter
    def size(self, value):
        if isinstance(value, (int, float)):
            self.__size = value
        else:
            raise TypeError('TypeError. Expected "int" or "float" type')

    def __str__(self):
        return f'{self.__name} pizza in size of {self.__size} centimeters'


class PizzaOfTheDay(Pizza):
    def __init__(self, day_of_the_week, size):
        self.__dotw = self.dotw_interpreter(day_of_the_week)
        match self.__dotw:
            case 1: super().__init__('Cheese', size)
            case 2: super().__init__('Veggie', size)
            case 3: super().__init__('Pepperoni', size)
            case 4: super().__init__('Meat', size)
            case 5: super().__init__('Margherita', size)
            case 6: super().__init__('BBQ Chicken', size)
            case 7: super().__init__('Supreme', size)
            case 0: raise ValueError('This is not a day of the week!')

    @staticmethod
    def dotw_interpreter(dotw):
        if isinstance(dotw, str):
            if dotw == "Monday" or dotw == "monday" or dotw == "Mon" or dotw == "mon" or dotw == "1":
                return 1
            elif dotw == "Tuesday" or dotw == "tuesday" or dotw == "Tue" or dotw == "tue" or dotw == "2":
                return 2
            elif dotw == "Wednesday" or dotw == "wednesday" or dotw == "Wed" or dotw == "wed" or dotw == "3":
                return 3
            elif dotw == "Thursday" or dotw == "thursday" or dotw == "Thu" or dotw == "thu" or dotw == "4":
                return 4
            elif dotw == "Friday" or dotw == "firday" or dotw == "Fri" or dotw == "fri" or dotw == "5":
                return 5
            elif dotw == "Saturday" or dotw == "saturday" or dotw == "Sat" or dotw == "sat" or dotw == "6":
                return 6
            elif dotw == "Sunday" or dotw == "sunday" or dotw == "Sun" or dotw == "sun" or dotw == "7":
                return 7
            else:
                return 0
        elif isinstance(dotw, int):
            if dotw == 7:  # тут заюзати регекс
                return dotw
            else:
                return ValueError('ValueError. Numbers from 1 to 7 expected')
        else:
            raise TypeError('TypeError. "str" or "int"/"float" type expected')


def main():
    pizza1 = PizzaOfTheDay('5', 50)
    print('An order is:')
    print(pizza1)

    pizza2 = PizzaOfTheDay(7, 40)
    print('An order is:')
    print(pizza2)


main()
