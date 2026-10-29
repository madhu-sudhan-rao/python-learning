def printEvenIndices(str):
    length = len(str)

    for i in range(0, length, 2):
        print(str[i], end='')

word = printEvenIndices(input("Enter a string: "))