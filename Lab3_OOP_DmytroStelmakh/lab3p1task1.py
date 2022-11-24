import argparse
import operator
import math


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("function", type=str)
    parser.add_argument("values", nargs='+')

    args = parser.parse_args()

    try:
        for ch in range(len(args.values)):
            args.values = list(map(float, args.values))
    except ValueError:
        print("Неправильні типи арументів")
        return

    operation = None
    try:
        operation = getattr(operator, args.function)
    except AttributeError:
        print("Немає такої операції")
        return

    try:
        operation = getattr(math, args.function)
    except AttributeError:
        print("Немає такої операції")
        return

    try:
        print(operation(*args.values))  # розкладаємо масив на окремі параметри за допомогою астеріска
    except TypeError:
        print("Неправильна кількість аргументів")

    return


main()
