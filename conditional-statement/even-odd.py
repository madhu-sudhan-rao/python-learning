x = int(input("Enter a number: "))


isEven = (x % 2) == 0

if(isEven):
    print(x, "is even")
else:
    print(x, "is odd")

def checkOddEven(x):
    if(x % 2 == 0):
        print(x, "is even")
        return
    else:
        print(x, "is odd")
        return