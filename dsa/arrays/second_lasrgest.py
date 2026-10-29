def second_largest(array):
    largest = -1
    second_large = -1
    
    for i in range(0, len(array)):
        if( array[i] > largest ):
            second_large = largest
            largest = array[i]
        elif( array[i] > second_large and array[i] < largest):
            second_large = array[i]
    return second_large

print(second_largest([1,2,3,4,5]))