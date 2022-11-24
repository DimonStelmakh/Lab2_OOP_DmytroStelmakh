class Composition:
    def __init__(self):
        self.goods = ['apple', 'banana', 'orange']
        self.quantity = {
            'apple': 40,
            'banana': 35,
            'orange': 33
        }
        self.price = {
            'apple': 30,
            'banana': 60,
            'orange': 45
        }

    def __str__(self):
        all_goods = ''
        for item in self.goods:
            all_goods += (f"Товар: {item}, в наявності: {self.quantity[item]} кг за ціною "
                          f"{self.price[item]} ₴/кг\n")
        return all_goods


def main():
    stock = Composition()
    print(stock)


main()
