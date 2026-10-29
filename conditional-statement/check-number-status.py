
def checkStatus( first, second, flag):
    if (first < 0 or second < 0 and not flag): 
        return True
    elif (first < 0 or second < 0 and flag):
        return True
    else:
        return False
    
first = int(input("Enter first number: "))
second = int(input("Enter second number: "))
flag = bool(input("Enter flag: "))


print(checkStatus(first, second, flag))