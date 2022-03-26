from cs50 import get_float
from math import floor


def main():
    # ask the user for the amount owed
    while True:
        dollars_owed = get_float("Change owed: ")
        cents_owed = floor(dollars_owed * 100)

        if cents_owed > 0:
            break
    # breakdown of all the coins, see cash.c
    quarters = cents_owed // 25
    dimes = (cents_owed % 25) // 10
    nickels = ((cents_owed % 25) % 10) // 5
    pennies = ((cents_owed % 25) % 10) % 5
    # sum of all the coins we owed
    print(f"{quarters + dimes + nickels + pennies}")


if __name__ == "__main__":
    main()
