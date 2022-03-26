# so we can use argv like in C
import sys
from cs50 import get_string


def main():
    # if there's no argument, print how to use it
    if len(sys.argv) != 2:
        print("Usage: ./caesar k")
        sys.exit(1)
    # get the plaintext to be encrypted
    k = int(sys.argv[1])
    plaintext = get_string("plaintext: ")

    print("ciphertext: ", end="")

    for ch in plaintext:
        # if is not an alphanumeric entry quit the program
        # else continue
        if not ch.isalpha():
            # That end="" line just overrides Python’s default behavior when printing which,
            # unlike C, tacks on a newline by default!
            print(ch, end="")
            continue
        # this is different from the C implementation
        # here we just using an offset of the ascii table
        # we assign 65 to A else 97 to a
        ascii_offset = 65 if ch.isupper() else 97
       # The ord() method returns an integer representing the Unicode
       # code point of the given Unicode character.
       # substract from the offset
        pi = ord(ch) - ascii_offset
        # put the result into a new variable,
        # add the number(cypher) to it and then use modulo to
        # wrap around the alpahbet
        ci = (pi + k) % 26
        # chr() is the opposite of ord()
        # The chr() method returns a character (a string) from an integer
        # (represents unicode code point of the character).
        print(chr(ci + ascii_offset), end="")
    # print a new line
    print()

    return 0


if __name__ == "__main__":
    main()
