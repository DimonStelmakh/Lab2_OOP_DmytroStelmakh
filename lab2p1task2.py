from datetime import datetime

pizza_types = ['Cheese', 'Veggie', 'Pepperoni', 'Meat', 'Margherita', 'BBQ Chicken', 'Supreme']
sizes = [30, 40, 50]
extra_ingredients_list = ['Meat', 'Cheese', 'Mushrooms', 'Broccoli', 'Pineapple', 'Onion']


class PriceDescriptor:
    def __init__(self):
        self.base_value = {
            "Cheese": 200,
            "Veggie": 180,
            "Pepperoni": 210,
            "Meat": 230,
            "Margherita": 200,
            "BBQ Chicken": 220,
            "Supreme": 240
        }

        self.size_coefs = {
            30: 1,
            40: 1.4,
            50: 1.8
        }

        self.extra_ingredients_values = {
            "Meat": 30,
            "Cheese": 25,
            "Mushrooms": 20,
            "Broccoli": 20,
            "Pineapple": 25,
            "Onion": 15
        }

    def __get__(self, instance_self, instance_class):
        real_price = self.base_value[instance_self.name] * self.size_coefs[instance_self.size]

        real_extras_price = 0
        if isinstance(instance_self.extra_ingredients, list):
            for item in instance_self.extra_ingredients:
                real_extras_price += self.extra_ingredients_values[item] * self.size_coefs[instance_self.size]

        real_price += real_extras_price
        return real_price


class Pizza:

    def __init__(self, name, size, extra_ingredients=None):
        self.name = name
        self.size = size
        self.extra_ingredients = extra_ingredients

    __real_price = PriceDescriptor()

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
    def real_price(self):
        return self.__real_price

    @name.setter
    def name(self, value):
        self.__name = value

    @size.setter
    def size(self, value):
        self.__size = value

    @extra_ingredients.setter
    def extra_ingredients(self, value):
        self.__extra_ingredients = value

    def __str__(self):
        if not self.__extra_ingredients:
            return f'{self.__name} pizza in size of {self.__size} centimeters'
        else:
            return f'{self.__name} pizza with extra {self.__extra_ingredients} in size of {self.__size} centimeters'


class PizzaOfTheDay(Pizza):

    pizza_of_the_day = {
        1: "Cheese",
        2: "Veggie",
        3: "Pepperoni",
        4: "Meat",
        5: "Margherita",
        6: "BBQ Chicken",
        7: "Supreme"
    }

    def __init__(self, day_of_the_week, size, extra_ingredients=None):
        super().__init__(self.pizza_of_the_day[day_of_the_week], size, extra_ingredients)


class Order:
    def __init__(self, first_pizza):
        if isinstance(first_pizza, Pizza):
            self.__pizzas = [first_pizza]
            self.__total_value = int(first_pizza.real_price)
        else:
            raise TypeError('Type "Pizza" needed to construct an order!')

    def __str__(self):
        aboba = "\n"
        return f'Your order is:\n{"".join(map(lambda x: str(x) + aboba, self.__pizzas))}' \
               f'\nThe total value is: {self.__total_value} UAH'

    def add_pizza(self, pizza):
        if isinstance(pizza, Pizza):
            self.__pizzas.append(pizza)
        else:
            raise TypeError('Expected an object of "Pizza".')
        self.__total_value += int(pizza.real_price)

    def remove_last_pizza(self):
        self.__pizzas.pop()


def answer_interpreter(answer):
    return True if answer in ('yes', 'yeah', 'y', 'Yes', 'Yeah', 'Y', 'Так', 'так', 'Да', 'да', 'д', 'т', 'Д', 'Т', '+',
                              'угу', 'ага') else False


def set_pizza_type():
    pizza_type = None
    success = False
    while not success:
        print(f'Available pizzas: {pizza_types}')
        pizza_type = input('Choose pizza: ')
        if pizza_type in pizza_types:
            success = True
        else:
            print(f'\033[93mThis pizza is not available!\033[0m')
    return pizza_type


def set_size():
    size = 30
    success = False
    while not success:
        print(f'Available sizes: {sizes}')
        try:
            size = int(input('Choose size: '))
        except ValueError:
            print('\033[93mEnter a number!\033[0m')
        else:
            if size in sizes:
                success = True
            else:
                print(f'\033[93mThis size is not available!\033[0m')
    return size


def set_extra_ingredients():
    extra_ingredients = None
    success = False
    while not success:
        print(f'Available extra ingredients: {extra_ingredients_list}')
        extra_ingredients_input = input('Add some coma-separated extra ingredients if you want '
                                        f'(or press Enter to skip): ').split(', ')
        if extra_ingredients_input[0] != '':
            extra_ingredients = []
            appending_error = False
            for item in extra_ingredients_input:
                if item in extra_ingredients_list:
                    extra_ingredients.append(item)
                else:
                    print(f'\033[93mAn ingredient {item} is not available.\033[0m')
                    appending_error = True
            if not appending_error:
                success = True
        else:
            success = True
    return extra_ingredients


def main():
    try_pizza_of_the_day = answer_interpreter(input('Do you want to try our Pizza Of The Day? (+/-): '))

    today = 0
    if try_pizza_of_the_day:
        today = datetime.today().weekday() + 1
        print(f'Today it\'s a {PizzaOfTheDay.pizza_of_the_day[today]} pizza!')

        size = set_size()
        extra_ingredients = set_extra_ingredients()

        order = Order(PizzaOfTheDay(today, size, extra_ingredients))
    else:
        pizza_type = set_pizza_type()
        size = set_size()
        extra_ingredients = set_extra_ingredients()

        order = Order(Pizza(pizza_type, size, extra_ingredients))

    print('\n\033[92mThe pizza has been added successfully!\033[0m', order, sep='\n')

    continuation = answer_interpreter(input('\nDo you want to order one more pizza?: '))
    while continuation:
        if not try_pizza_of_the_day:
            order.add_pizza(Pizza(set_pizza_type(), set_size(), set_extra_ingredients()))
        else:
            of_the_day = answer_interpreter(input('One more pizza of the day?: '))
            if of_the_day:
                order.add_pizza(PizzaOfTheDay(today, set_size(), set_extra_ingredients()))
            else:
                order.add_pizza(Pizza(set_pizza_type(), set_size(), set_extra_ingredients()))

        print('\n\033[92mThe pizza has been added successfully!\033[0m', order, sep='\n')

        continuation = answer_interpreter(input('\nDo you want to order one more pizza?: '))

    print('\n\033[92mYour order has been completely formed successfully!\033[0m', order, sep='\n')


main()
