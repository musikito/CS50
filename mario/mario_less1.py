import cs50
# prompt user for height
while True:
    height = cs50.get_int("Height: ")
    #height = int(input("Height: "))
    if height > 0 and height <= 8:
        break

# print pyramid
for i in range(height):
    for j in range(1, height-i):
        print(" ", end="")

    for b in range(1, i+2):
        print("#", end="")
    print()
