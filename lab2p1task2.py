from datetime import datetime


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
        try:
            self.__size = int(value)
        except ValueError:
            raise ValueError('Expected a number')

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
        # self.__dotw = self.dotw_interpreter(day_of_the_week)

        pizza_of_the_day = {
            1: "Cheese",
            2: "Veggie",
            3: "Pepperoni",
            4: "Meat",
            5: "Margherita",
            6: "BBQ Chicken",
            7: "Supreme"
        }

        super().__init__(pizza_of_the_day[day_of_the_week], size, extra_ingredients)


class Order:
    def __init__(self, first_pizza):
        self.pizzas = [first_pizza]
        self.total_value = 0

    def __str__(self):
        return f'PIZZA'

    def add_pizza(self, pizza):
        if isinstance(pizza, Pizza):
            self.pizzas.append(pizza)
        else:
            raise TypeError


def answer_interpreter(answer):
    return True if answer in ('yes', 'yeah', 'y', 'Yes', 'Yeah', 'Y', 'Так', 'так', 'Да', 'да', 'д', 'т', 'Д', 'Т', '+',
                              'угу', 'ага') else False


def main():
    if answer_interpreter(input('Do you want to try our Pizza Of The Day? (+/-): ')):
        pizza = PizzaOfTheDay(datetime.today().weekday()+1, input('Enter a size in centimeters: '),
                              input('Add some extra ingredients if you want (or just press Enter to skip): '))
    else:
        pizza = Pizza(input('Enter a name of pizza: '), input('Enter a size in centimeters: '),
                      input('Add some extra ingredients if you want (or just press Enter to skip): '))

    print('\n\033[92mYour order has been formed successfully!\033[0m', pizza, sep='\n')


main()
