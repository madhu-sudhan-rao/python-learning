def sumOfNaturalNumbersFormula(n):
    numerator = n * (n + 1)
    denominator = 2
    result = numerator / denominator
    return result

def sumOfNaturalNumbersManual(n):

    for j in range(1, n+1 ):
        values = []
        for i in range(1, j + 1):
            print(i,sep=' ', end=' ')
            if(i < j):
                print('+', sep=' ', end=' ')
            values.append(i)

        print("=", sum(values))

sumOfNaturalNumbersManual(5)
    
