# so we can use argv like in C
import sys
from cs50 import get_string


def is_valid(k):
    # function to check if argument is valid
    for ch in k:
        if not ch.isalpha():
            return False
    return True


def main():
    # check for arguments and if not print the usage
    if len(sys.argv) != 2 or not is_valid(sys.argv[1]):
        print("Usage: ./vigenere k")
        sys.exit(1)
    # get the plaintext to be encrypted
    k = sys.argv[1]
    plaintext = get_string("plaintext: ")
    j = 0

    print("ciphertext: ", end="")

    for ch in plaintext:
        if not ch.isalpha():
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
        # now we will get the int for the ciphertext
        # and use the modulo plaintext
        kj = ord(k[j % len(k)].upper()) - 65
        # print(kj)
        # put the result into a new variable,
        # add the number(cypher) to it and then use modulo to
        # wrap around the alpahbet
        ci = (pi + kj) % 26
        # increment by the cypher given
        j += 1

        print(chr(ci + ascii_offset), end="")

    print()

    return 0


if __name__ == "__main__":
    main()
