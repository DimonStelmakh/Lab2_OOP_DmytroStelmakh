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
        if not value:
            self.__extra_ingredients = None
        elif isinstance(value, (str, list)):
            self.__extra_ingredients = value
        else:
            raise TypeError('Expected "str" or "list" type')

    def __str__(self):
        if not self.__extra_ingredients:
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
        if dotw in ("Monday", "monday", "Mon", "mon", "First", "first", "1"):
            return 1
        elif dotw in ("Tuesday", "tuesday", "Tue", "tue", "2"):
            return 2
        elif dotw in ("Wednesday", "wednesday", "Wed", "wed", "3"):
            return 3
        elif dotw in ("Thursday", "thursday", "Thu", "thu", "4"):
            return 4
        elif dotw in ("Friday", "firday", "Fri", "fri", "5"):
            return 5
        elif dotw in ("Saturday", "saturday", "Sat", "sat", "6"):
            return 6
        elif dotw in ("Sunday", "sunday", "Sun", "sun", "Last", "last", "7"):
            return 7
        else:
            return 0


def main():
    pizza1 = PizzaOfTheDay('5', 50)
    print('An order №1 is:')
    print(pizza1)

    pizza2 = PizzaOfTheDay('7', 40)
    print('An order №2 is:')
    print(pizza2)

    pizza3 = PizzaOfTheDay('tue', 35, 'mushrooms')
    print('An order №3 is:')
    print(pizza3)

    pizza4 = PizzaOfTheDay('Wednesday', 40, 'pineapple')
    print('An order №4 is:')
    print(pizza4)


main()
