class Pizza:
    def __init__(self, name, size, extra_ingredients=None):
        self.name = name
        self.size = size
        self.extra_ingredients = extra_ingredients

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size

    @property
    def extra_ingredients(self):
        return self.__extra_ingredients

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError('Expected "str" type')

    @size.setter
    def size(self, value):
        if isinstance(value, (int, float)):
            self.__size = value
        else:
            raise TypeError('Expected "int" or "float" type')

    @extra_ingredients.setter
    def extra_ingredients(self, value):
        if value is None:
            self.__extra_ingredients = None
        elif isinstance(value, (str, list)):
            self.__extra_ingredients = value
        else:
            raise TypeError('Expected "str" or "list" type')

    def __str__(self):
        if self.__extra_ingredients is None:
            return f'{self.__name} pizza in size of {self.__size} centimeters'
        else:
            return f'{self.__name} pizza with extra {self.__extra_ingredients} in size of {self.__size} centimeters'


class PizzaOfTheDay(Pizza):
    def __init__(self, day_of_the_week, size, extra_ingredients=None):
        self.__dotw = self.dotw_interpreter(day_of_the_week)
        match self.__dotw:
            case 1: super().__init__('Cheese', size, extra_ingredients)
            case 2: super().__init__('Veggie', size, extra_ingredients)
            case 3: super().__init__('Pepperoni', size, extra_ingredients)
            case 4: super().__init__('Meat', size, extra_ingredients)
            case 5: super().__init__('Margherita', size, extra_ingredients)
            case 6: super().__init__('BBQ Chicken', size, extra_ingredients)
            case 7: super().__init__('Supreme', size, extra_ingredients)
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
            if 1 <= dotw <= 7:
                return dotw
            else:
                raise ValueError('Numbers from 1 to 7 expected')
        else:
            raise TypeError('"str" or "int"/"float" type expected')


def main():
    pizza1 = PizzaOfTheDay('5', 50)
    print('An order №1 is:')
    print(pizza1)

    pizza2 = PizzaOfTheDay(7, 40)
    print('An order №2 is:')
    print(pizza2)

    pizza3 = PizzaOfTheDay('tue', 35, 'mushrooms')
    print('An order №3 is:')
    print(pizza3)

    pizza4 = PizzaOfTheDay('Wednesday', 40, 'pineapple')
    print('An order №4 is:')
    print(pizza4)


main()
