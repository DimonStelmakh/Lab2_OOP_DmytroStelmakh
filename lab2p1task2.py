from datetime import datetime


class Pizza:

    __pizza_types = ['Cheese', 'Veggie', 'Pepperoni', 'Meat', 'Margherita', 'BBQ Chicken', 'Supreme']
    __sizes = [30, 40, 50]
    __base_value = {
        "Cheese": 200,
        "Veggie": 180,
        "Pepperoni": 210,
        "Meat": 230,
        "Margherita": 200,
        "BBQ Chicken": 220,
        "Supreme": 240
    }

    __size_coefs = {
        30: 1,
        40: 1.4,
        50: 1.8
    }

    __extra_ingredients = ['Meat', 'Cheese', 'Mushrooms', 'Broccoli', 'Pineapple', 'Onion']

    __extra_ingredients_valus = {
        "Meat": 30,
        "Cheese": 25,
        "Mushrooms": 20,
        "Brocolli": 20,
        "Pineapple": 25,
        "Onion": 15
    }

    def __init__(self, name, size, extra_ingredients=None):
        self.name = name
        self.size = size
        self.extra_ingredients = extra_ingredients
        self.value = self.__base_value[self.name]

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size

    @property
    def extra_ingredients(self):
        return self.__extra_ingredients

    @property
    def value(self):
        return self.__value

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            if value in self.__pizza_types:
                self.__name = value
            else:
                raise ValueError(f'No such pizza. Available pizzas: {self.__pizza_types}')
        else:
            raise TypeError('Expected "str" type.')

    @size.setter
    def size(self, value):
        try:
            value = int(value)
        except ValueError:
            print('Expected a number.')
        if value in self.__sizes:
            self.__size = int(value)
        else:
            raise ValueError(f'No such size. Available sizes: {self.__sizes}')

    @extra_ingredients.setter
    def extra_ingredients(self, value):
        if not value:
            self.__extra_ingredients = None
        elif isinstance(value, (str, list)):
            if value in self.__extra_ingredients:
                self.__extra_ingredients = value
            else:
                raise ValueError('There is no such extra ingredient!\n'
                                 f'Here is the list of all available extra ingredients:\n{self.__extra_ingredients}')
        else:
            raise TypeError('Expected "str" or "list" type.')

    @value.setter
    def value(self, value):
        if isinstance(value, (int, float)):
            if value >= 0:
                self.__value = value
            else:
                raise ValueError('The price cannot be less than 0.')
        else:
            raise TypeError('Expected "int" or "float" type of value.')

    def __str__(self):
        if not self.__extra_ingredients:
            return f'{self.__name} pizza in size of {self.__size} centimeters'
        else:
            return f'{self.__name} pizza with extra {self.__extra_ingredients} in size of {self.__size} centimeters'


class PizzaOfTheDay(Pizza):
    def __init__(self, day_of_the_week, size, extra_ingredients=None):

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
        self.__pizzas = [first_pizza]
        self.__total_value = first_pizza.value

    def __str__(self):
        aboba = "\n"
        return f'Your order is:\n{"".join(map(lambda x: str(x) + aboba, self.__pizzas))}' \
               f'\nThe total value is: {self.__total_value} UAH'

    def add_pizza(self, pizza):
        if isinstance(pizza, Pizza):
            self.__pizzas.append(pizza)
        else:
            raise TypeError('Expected an object of "Pizza".')
        self.__total_value += pizza.value

    def remove_last_pizza(self):
        self.__pizzas.pop()


def answer_interpreter(answer):
    return True if answer in ('yes', 'yeah', 'y', 'Yes', 'Yeah', 'Y', 'Так', 'так', 'Да', 'да', 'д', 'т', 'Д', 'Т', '+',
                              'угу', 'ага') else False


def main():
    if answer_interpreter(input('Do you want to try our Pizza Of The Day? (+/-): ')):
        order = Order(PizzaOfTheDay(datetime.today().weekday()+1, input('Enter a size in centimeters (30/40/50): '),
                      input(f'Add some extra ingredients if you want (or just press Enter to skip): ')))
    else:
        order = Order(Pizza(input('Enter a name of the pizza: '), input('Enter a size in centimeters (30/40/50): '),
                      input('Add some extra ingredients if you want (or just press Enter to skip): ')))
    print('\n\033[92mThe pizza has been added successfully!\033[0m', order, sep='\n')

    continuation = answer_interpreter(input('\nDo you want to order one more pizza?: '))
    while continuation:
        of_the_day = answer_interpreter(input('One more pizza of the day?: '))
        if of_the_day:
            order.add_pizza(PizzaOfTheDay(datetime.today().weekday()+1,
                            input('Enter a size in centimeters (30/40/50): '),
                            input('Add some extra ingredients if you want (or just press Enter to skip): ')))
        else:
            order.add_pizza(Pizza(input('Enter a name of the pizza: '),
                            input('Enter a size in centimeters (30/40/50): '),
                            input('Add some extra ingredients if you want (or just press Enter to skip): ')))
        print('\n\033[92mThe pizza has been added successfully!\033[0m\n', order)

        continuation = answer_interpreter(input('\nDo you want to order one more pizza?: '))

    print('\n\033[92mYour order has been formed successfully!\033[0m\n', order)


main()
