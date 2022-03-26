import cs50

def main():
    while True:
        #print("Height: ", end = "")
        height = cs50.get_int("Height: ")
        if height > 0 and height <= 8:
            break

    for i in range(height):
        for j in range(height - i - 1):
            print(" ", end = "")
        for k in range(i+2):
            print("#", end = "")
        print("")

if __name__ == "__main__":
    main()
