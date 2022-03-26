from cs50 import get_int
from math import floor


def main():
    digit1 = 0
    digit2 = 0
    num_digits = 0
    sum_of_double_odds = 0
    sum_of_evens = 0
    # ask for the card number
    cc_number = get_int("Number: ")

    while cc_number > 0:
        digit2 = digit1
        digit1 = cc_number % 10
        # get the evens
        if num_digits % 2 == 0:
            sum_of_evens += digit1
        else:
            # we get the odds
            multiple = 2 * digit1
            sum_of_double_odds += (multiple // 10) + (multiple % 10)

        cc_number //= 10
        num_digits += 1
    # if the result is == 0 then we have a valid card
    is_valid = (sum_of_evens + sum_of_double_odds) % 10 == 0
    first_two_digits = (digit1 * 10) + digit2
    # this is the same implementation as credit.c
    # VISA is the easiest to find out
    if digit1 == 4 and num_digits >= 13 and num_digits <= 16 and is_valid:
        print("VISA\n")
    elif first_two_digits >= 51 and first_two_digits <= 55 and num_digits == 16 and is_valid:
        print("MASTERCARD\n")
    elif (first_two_digits == 34 or first_two_digits == 37) and num_digits == 15 and is_valid:
        print("AMEX\n")
    else:
        print("INVALID\n")


if __name__ == "__main__":
    main()
